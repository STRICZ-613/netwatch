"""
Services module for NetWatch backend.
Contains scanner, simulator, and monitor services.
"""

from .scanner import arp_scan, get_bandwidth_stats
from .simulator import (
    get_simulated_devices,
    get_simulated_bandwidth,
    get_simulated_ports,
    inject_unknown_device
)
from .monitor import NetworkMonitor

__all__ = [
    "arp_scan",
    "get_bandwidth_stats",
    "get_simulated_devices",
    "get_simulated_bandwidth",
    "get_simulated_ports",
    "inject_unknown_device",
    "NetworkMonitor"
]