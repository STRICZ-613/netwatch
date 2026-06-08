"""
Network monitoring service.
Runs in background, continuously scans network and detects unknown devices.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime

# Import configuration
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import USE_REAL_SCANNER, SCAN_INTERVAL, NETWORK_RANGE, validate_config

# Import scanner/simulator
from services.scanner import arp_scan, get_bandwidth_stats
from services.simulator import (
    get_simulated_devices,
    get_simulated_bandwidth,
    inject_unknown_device
)

# Configure logging
logger = logging.getLogger(__name__)


class NetworkMonitor:
    """
    Background network monitoring service.

    Responsibilities:
    - Periodically scan the network (real or simulated)
    - Compare current state with previous state
    - Detect new/unknown devices
    - Generate events for DB storage
    - Broadcast alerts via WebSocket
    """

    def __init__(self):
        """Initialize the network monitor."""
        self.is_running = False
        self.monitor_task: Optional[asyncio.Task] = None
        self.known_devices_cache: Dict[str, Dict[str, Any]] = {}
        self.callbacks: List[Callable] = []

        # Validate configuration on startup
        config_status = validate_config()
        if not config_status["valid"]:
            logger.error(f"Configuration errors: {config_status['errors']}")
            raise RuntimeError("Invalid configuration")

        logger.info(f"NetworkMonitor initialized in {config_status['mode']} mode")
        for warning in config_status["warnings"]:
            logger.warning(warning)

    def register_callback(self, callback: Callable):
        """
        Register a callback function to be called when events occur.
        Used by the WebSocket manager to broadcast events to clients.

        Args:
            callback: Async function that accepts an event dict
        """
        self.callbacks.append(callback)
        logger.debug(f"Callback registered. Total: {len(self.callbacks)}")

    async def _notify_callbacks(self, event: Dict[str, Any]):
        """
        Notify all registered callbacks of an event.

        Args:
            event: Event dictionary with 'type' and 'data' fields
        """
        for callback in self.callbacks:
            try:
                await callback(event)
            except Exception as e:
                logger.error(f"Callback failed: {str(e)}")

    def _get_current_devices(self) -> List[Dict[str, Any]]:
        """
        Get current network devices based on configuration mode.

        Returns:
            List of device dictionaries
        """
        if USE_REAL_SCANNER:
            logger.debug("Performing real ARP scan...")
            raw_devices = arp_scan(NETWORK_RANGE)

            # Convert to standard format
            devices = []
            for d in raw_devices:
                devices.append({
                    "mac": d["mac"],
                    "ip": d["ip"],
                    "name": d.get("name", d["ip"]),
                    "category": "Unknown",
                    "is_known": False,
                    "status": "online"
                })
            return devices
        else:
            logger.debug("Getting simulated devices...")
            return get_simulated_devices()

    def _get_current_bandwidth(self) -> Dict[str, float]:
        """
        Get current bandwidth usage based on configuration mode.

        Returns:
            Dictionary with 'upload' and 'download' keys
        """
        if USE_REAL_SCANNER:
            return get_bandwidth_stats()
        else:
            return get_simulated_bandwidth()

    def _detect_changes(
            self,
            current_devices: List[Dict[str, Any]],
            previous_devices: Dict[str, Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Detect changes between current and previous device states.

        Args:
            current_devices: List of current devices
            previous_devices: Dict mapping MAC to previous device state

        Returns:
            Dictionary with 'new', 'disappeared', 'status_changed' keys
        """
        current_by_mac = {d["mac"]: d for d in current_devices}
        previous_macs = set(previous_devices.keys())
        current_macs = set(current_by_mac.keys())

        # New devices
        new_macs = current_macs - previous_macs
        new_devices = [current_by_mac[mac] for mac in new_macs]

        # Disappeared devices (went offline)
        disappeared_macs = previous_macs - current_macs
        disappeared_devices = [previous_devices[mac] for mac in disappeared_macs]

        # Status changes (online/offline)
        status_changes = []
        for mac in current_macs & previous_macs:
            current_status = current_by_mac[mac].get("status", "unknown")
            previous_status = previous_devices[mac].get("status", "unknown")

            if current_status != previous_status:
                status_changes.append({
                    "device": current_by_mac[mac],
                    "old_status": previous_status,
                    "new_status": current_status
                })

        return {
            "new": new_devices,
            "disappeared": disappeared_devices,
            "status_changed": status_changes
        }

    def _create_device_event(
            self,
            device: Dict[str, Any],
            event_type: str,
            description: str
    ) -> Dict[str, Any]:
        """
        Create a standardized event dictionary for database storage and WebSocket broadcast.

        Args:
            device: Device dictionary
            event_type: Type of event (e.g., 'device_connected', 'unknown_device_detected')
            description: Human-readable description

        Returns:
            Event dictionary
        """
        return {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "device": {
                "mac": device["mac"],
                "ip": device.get("ip", "unknown"),
                "name": device.get("name", "Unknown"),
                "category": device.get("category", "Unknown"),
                "is_known": device.get("is_known", False)
            },
            "description": description
        }

    async def _process_scan_results(
            self,
            current_devices: List[Dict[str, Any]],
            previous_devices: Dict[str, Dict[str, Any]]
    ):
        """
        Process scan results, detect events, and trigger callbacks.

        Args:
            current_devices: Current device list
            previous_devices: Previous device state cache
        """
        changes = self._detect_changes(current_devices, previous_devices)

        # Handle new devices (including unknown ones)
        for device in changes["new"]:
            is_known = device.get("is_known", False)

            if not is_known:
                # Unknown device detected - CRITICAL ALERT
                event = self._create_device_event(
                    device,
                    "unknown_device_detected",
                    f"UNKNOWN DEVICE: {device['name']} ({device['ip']}) connected to the network"
                )
                logger.warning(f"ALERT: {event['description']}")
                await self._notify_callbacks(event)
            else:
                # Known device connected
                event = self._create_device_event(
                    device,
                    "device_connected",
                    f"Device {device['name']} connected to the network"
                )
                logger.info(f"Device connected: {device['name']}")
                await self._notify_callbacks(event)

        # Handle devices that disappeared (went offline)
        for device in changes["disappeared"]:
            event = self._create_device_event(
                device,
                "device_disconnected",
                f"Device {device['name']} disconnected from the network"
            )
            logger.info(f"Device disconnected: {device['name']}")
            await self._notify_callbacks(event)

        # Handle status changes
        for change in changes["status_changed"]:
            device = change["device"]
            event = self._create_device_event(
                device,
                "device_status_changed",
                f"Device {device['name']} went {change['new_status']}"
            )
            logger.debug(f"Status change: {device['name']} -> {change['new_status']}")
            await self._notify_callbacks(event)

    async def _monitor_loop(self):
        """
        Main monitoring loop. Runs continuously until stopped.
        """
        logger.info("Monitor loop started")

        # Initialize with empty state
        previous_devices: Dict[str, Dict[str, Any]] = {}

        while self.is_running:
            try:
                # Get current network state
                current_devices = self._get_current_devices()

                # Process changes if we have previous data
                if previous_devices:
                    await self._process_scan_results(current_devices, previous_devices)

                # Update cache for next iteration
                previous_devices = {d["mac"]: d for d in current_devices}

                # Broadcast bandwidth data
                bandwidth = self._get_current_bandwidth()
                bandwidth_event = {
                    "type": "bandwidth_update",
                    "timestamp": datetime.now().isoformat(),
                    "data": bandwidth
                }
                await self._notify_callbacks(bandwidth_event)

                # Wait before next scan
                await asyncio.sleep(SCAN_INTERVAL)

            except Exception as e:
                logger.error(f"Monitor loop error: {str(e)}")
                await asyncio.sleep(SCAN_INTERVAL)

        logger.info("Monitor loop stopped")

    async def start(self):
        """Start the background monitoring service."""
        if self.is_running:
            logger.warning("Monitor is already running")
            return

        self.is_running