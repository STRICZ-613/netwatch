"""
Real network scanner module.
Performs ARP scans and bandwidth monitoring using system tools.
Requires admin/root privileges for ARP scanning.
"""

import time
import logging
from typing import List, Dict, Any, Optional

# Configure logging
logger = logging.getLogger(__name__)

# Try to import optional dependencies
try:
    from scapy.all import ARP, Ether, srp

    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    logger.warning("scapy not available. ARP scanning will be disabled.")

try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logger.warning("psutil not available. Bandwidth monitoring will be disabled.")

# Network interface stats cache for bandwidth calculation
_last_net_stats: Dict[str, Any] = {}
_last_net_time: Optional[float] = None


def arp_scan(network_range: str, timeout: int = 3) -> List[Dict[str, str]]:
    """
    Perform ARP scan to discover devices on the local network.

    Args:
        network_range: CIDR notation (e.g., "192.168.1.0/24")
        timeout: Seconds to wait for responses

    Returns:
        List of dictionaries with keys: 'ip', 'mac'
        Example: [{'ip': '192.168.1.10', 'mac': 'AA:BB:CC:DD:EE:FF'}, ...]

    Note:
        Requires admin/root privileges. Returns empty list if scapy is unavailable.
    """
    if not SCAPY_AVAILABLE:
        logger.error("Cannot perform ARP scan: scapy not installed")
        return []

    if not network_range:
        logger.error("Cannot perform ARP scan: no network range provided")
        return []

    try:
        # Create ARP request packet
        arp_request = ARP(pdst=network_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp_request

        # Send packet and receive responses
        logger.info(f"Scanning network: {network_range} (timeout: {timeout}s)")
        result = srp(packet, timeout=timeout, verbose=False, retry=2)[0]

        # Parse responses
        devices = []
        for sent, received in result:
            device = {
                'ip': received.psrc,
                'mac': received.hwsrc.upper()
            }
            devices.append(device)

        logger.info(f"ARP scan complete. Found {len(devices)} device(s)")
        return devices

    except PermissionError:
        logger.error("Permission denied for ARP scan. Run with admin/root privileges.")
        return []
    except Exception as e:
        logger.error(f"ARP scan failed: {str(e)}")
        return []


def get_bandwidth_stats(interface: Optional[str] = None) -> Dict[str, float]:
    """
    Get current network bandwidth usage (upload/download speeds in Mbps).

    Args:
        interface: Network interface name (e.g., 'eth0', 'wlan0').
                  If None, uses the first non-loopback interface.

    Returns:
        Dictionary with keys: 'upload', 'download' (values in Mbps)
        Example: {'upload': 1.23, 'download': 5.67}
    """
    global _last_net_stats, _last_net_time

    if not PSUTIL_AVAILABLE:
        logger.error("Cannot get bandwidth stats: psutil not installed")
        return {'upload': 0.0, 'download': 0.0}

    try:
        # Get network I/O counters
        net_io = psutil.net_io_counters(pernic=True)

        # Select interface
        if interface is None:
            # Auto-detect: use first interface with meaningful traffic
            for iface, stats in net_io.items():
                if iface.startswith(('lo', 'Loopback')):
                    continue
                interface = iface
                break
            if interface is None:
                interface = list(net_io.keys())[0]

        if interface not in net_io:
            logger.warning(f"Interface {interface} not found")
            return {'upload': 0.0, 'download': 0.0}

        current_stats = {
            'upload': net_io[interface].bytes_sent,
            'download': net_io[interface].bytes_recv
        }
        current_time = time.time()

        # Calculate speed if we have previous data
        if _last_net_stats is not None and _last_net_time is not None:
            time_delta = current_time - _last_net_time
            if time_delta > 0:
                # Bytes per second -> Megabits per second (1 byte = 8 bits)
                upload_mbps = (current_stats['upload'] - _last_net_stats['upload']) * 8 / time_delta / 1_000_000
                download_mbps = (current_stats['download'] - _last_net_stats['download']) * 8 / time_delta / 1_000_000

                # Ensure non-negative values (can happen due to counter reset)
                upload_mbps = max(0, upload_mbps)
                download_mbps = max(0, download_mbps)

                # Update cache
                _last_net_stats = current_stats
                _last_net_time = current_time

                return {'upload': round(upload_mbps, 2), 'download': round(download_mbps, 2)}

        # First call or no previous data
        _last_net_stats = current_stats
        _last_net_time = current_time
        return {'upload': 0.0, 'download': 0.0}

    except Exception as e:
        logger.error(f"Bandwidth stats failed: {str(e)}")
        return {'upload': 0.0, 'download': 0.0}


def get_hostname(ip: str, timeout: int = 2) -> str:
    """
    Attempt to resolve IP address to hostname.

    Args:
        ip: IP address as string
        timeout: Timeout in seconds

    Returns:
        Hostname if found, otherwise IP address
    """
    try:
        import socket
        socket.setdefaulttimeout(timeout)
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname.split('.')[0]  # Return short name
    except Exception:
        return ip


# Self-test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("=== REAL SCANNER TEST ===")
    print(f"scapy available: {SCAPY_AVAILABLE}")
    print(f"psutil available: {PSUTIL_AVAILABLE}")

    if PSUTIL_AVAILABLE:
        bw = get_bandwidth_stats()
        print(f"Bandwidth: {bw}")

    if SCAPY_AVAILABLE:
        devices = arp_scan("192.168.1.0/24", timeout=2)
        print(f"Devices found: {len(devices)}")
        for d in devices[:5]:
            print(f"  {d['ip']} -> {d['mac']}")