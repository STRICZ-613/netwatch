"""
Network simulator module.
Provides realistic fake data for demo mode when real scanning is disabled.
"""

import random
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

# ============================================================================
# STATIC SIMULATED DATA
# ============================================================================

# Realistic device database
SIMULATED_DEVICES_DB = [
    {
        "mac": "AA:BB:CC:DD:EE:01",
        "ip": "192.168.1.1",
        "name": "Routeur Principal",
        "category": "Network",
        "is_known": True,
        "device_type": "router"
    },
    {
        "mac": "AA:BB:CC:DD:EE:02",
        "ip": "192.168.1.10",
        "name": "PC-Thomas",
        "category": "Workstation",
        "is_known": True,
        "device_type": "computer"
    },
    {
        "mac": "AA:BB:CC:DD:EE:03",
        "ip": "192.168.1.11",
        "name": "MacBook-Sophie",
        "category": "Workstation",
        "is_known": True,
        "device_type": "laptop"
    },
    {
        "mac": "AA:BB:CC:DD:EE:04",
        "ip": "192.168.1.12",
        "name": "iPhone-Lucas",
        "category": "Mobile",
        "is_known": True,
        "device_type": "phone"
    },
    {
        "mac": "AA:BB:CC:DD:EE:05",
        "ip": "192.168.1.13",
        "name": "iPad-Family",
        "category": "Mobile",
        "is_known": True,
        "device_type": "tablet"
    },
    {
        "mac": "AA:BB:CC:DD:EE:06",
        "ip": "192.168.1.20",
        "name": "TV-Salon",
        "category": "Entertainment",
        "is_known": True,
        "device_type": "tv"
    },
    {
        "mac": "AA:BB:CC:DD:EE:07",
        "ip": "192.168.1.21",
        "name": "Chromecast",
        "category": "Entertainment",
        "is_known": True,
        "device_type": "streamer"
    },
    {
        "mac": "AA:BB:CC:DD:EE:08",
        "ip": "192.168.1.30",
        "name": "Imprimante-Laser",
        "category": "Peripheral",
        "is_known": True,
        "device_type": "printer"
    },
    {
        "mac": "AA:BB:CC:DD:EE:09",
        "ip": "192.168.1.31",
        "name": "NAS-Synology",
        "category": "Storage",
        "is_known": True,
        "device_type": "nas"
    },
    {
        "mac": "AA:BB:CC:DD:EE:10",
        "ip": "192.168.1.40",
        "name": "Enceinte-Google",
        "category": "IoT",
        "is_known": True,
        "device_type": "speaker"
    },
    {
        "mac": "AA:BB:CC:DD:EE:11",
        "ip": "192.168.1.41",
        "name": "Prise-Connectee",
        "category": "IoT",
        "is_known": True,
        "device_type": "smart_plug"
    },
    {
        "mac": "AA:BB:CC:DD:EE:12",
        "ip": "192.168.1.50",
        "name": "Console-PS5",
        "category": "Entertainment",
        "is_known": True,
        "device_type": "console"
    }
]

# Port scan results by device type
PORT_SCAN_TEMPLATES = {
    "router": [
        {"port": 22, "protocol": "tcp", "status": "open", "service": "SSH", "risk": "medium"},
        {"port": 80, "protocol": "tcp", "status": "open", "service": "HTTP", "risk": "low"},
        {"port": 443, "protocol": "tcp", "status": "open", "service": "HTTPS", "risk": "low"},
        {"port": 53, "protocol": "udp", "status": "open", "service": "DNS", "risk": "low"}
    ],
    "computer": [
        {"port": 22, "protocol": "tcp", "status": "open", "service": "SSH", "risk": "medium"},
        {"port": 80, "protocol": "tcp", "status": "open", "service": "HTTP", "risk": "low"},
        {"port": 443, "protocol": "tcp", "status": "open", "service": "HTTPS", "risk": "low"},
        {"port": 445, "protocol": "tcp", "status": "closed", "service": "SMB", "risk": "high"},
        {"port": 3389, "protocol": "tcp", "status": "closed", "service": "RDP", "risk": "high"}
    ],
    "laptop": [
        {"port": 22, "protocol": "tcp", "status": "filtered", "service": "SSH", "risk": "low"},
        {"port": 80, "protocol": "tcp", "status": "open", "service": "HTTP", "risk": "low"},
        {"port": 443, "protocol": "tcp", "status": "open", "service": "HTTPS", "risk": "low"}
    ],
    "phone": [
        {"port": 443, "protocol": "tcp", "status": "open", "service": "HTTPS", "risk": "low"}
    ],
    "tablet": [
        {"port": 443, "protocol": "tcp", "status": "open", "service": "HTTPS", "risk": "low"}
    ],
    "tv": [
        {"port": 80, "protocol": "tcp", "status": "open", "service": "HTTP", "risk": "low"},
        {"port": 554, "protocol": "tcp", "status": "open", "service": "RTSP", "risk": "medium"}
    ],
    "printer": [
        {"port": 80, "protocol": "tcp", "status": "open", "service": "HTTP", "risk": "low"},
        {"port": 515, "protocol": "tcp", "status": "open", "service": "LPD", "risk": "medium"},
        {"port": 9100, "protocol": "tcp", "status": "open", "service": "JetDirect", "risk": "high"}
    ],
    "nas": [
        {"port": 80, "protocol": "tcp", "status": "open", "service": "HTTP", "risk": "low"},
        {"port": 443, "protocol": "tcp", "status": "open", "service": "HTTPS", "risk": "low"},
        {"port": 445, "protocol": "tcp", "status": "open", "service": "SMB", "risk": "high"}
    ],
    "default": [
        {"port": 80, "protocol": "tcp", "status": "open", "service": "HTTP", "risk": "low"}
    ]
}

# Bandwidth history simulator
_bandwidth_history = []
_last_bandwidth_update = 0


def get_simulated_devices() -> List[Dict[str, Any]]:
    """
    Generate a realistic list of network devices for demo mode.

    Returns:
        List of device dictionaries with fields:
        - mac: MAC address
        - ip: IP address
        - name: Device name
        - category: Device category
        - is_known: Boolean
        - status: 'online' or 'offline' (randomized)
    """
    devices = []

    for device in SIMULATED_DEVICES_DB:
        # Randomize online/offline status (80% online)
        is_online = random.random() < 0.8

        devices.append({
            "mac": device["mac"],
            "ip": device["ip"],
            "name": device["name"],
            "category": device["category"],
            "is_known": device["is_known"],
            "status": "online" if is_online else "offline"
        })

    return devices


def get_simulated_bandwidth() -> Dict[str, float]:
    """
    Generate fluctuating bandwidth values for demo mode.
    Simulates realistic network traffic patterns.

    Returns:
        Dictionary with 'upload' and 'download' keys (values in Mbps)
    """
    global _last_bandwidth_update

    # Generate smooth random walk for realistic-looking traffic
    current_time = time.time()

    if not _bandwidth_history:
        # Initialize
        _bandwidth_history.append({"upload": 2.5, "download": 15.0})
        _last_bandwidth_update = current_time
    else:
        # Time delta affects step size
        delta = min(current_time - _last_bandwidth_update, 5.0)
        if delta > 0.5:
            # Random walk with drift
            last = _bandwidth_history[-1]

            # Upload: usually lower, occasional spikes
            upload_change = random.uniform(-1.5, 2.0) * delta
            new_upload = max(0.1, min(12.0, last["upload"] + upload_change))

            # Download: higher, with more variation
            download_change = random.uniform(-5.0, 8.0) * delta
            new_download = max(0.5, min(45.0, last["download"] + download_change))

            # Occasional burst (1 in 10 chance)
            if random.random() < 0.1 * delta:
                new_download += random.uniform(10, 30)
                new_upload += random.uniform(1, 5)

            _bandwidth_history.append({"upload": new_upload, "download": new_download})
            _last_bandwidth_update = current_time

            # Keep history limited
            while len(_bandwidth_history) > 60:
                _bandwidth_history.pop(0)

    return {
        "upload": round(_bandwidth_history[-1]["upload"], 2),
        "download": round(_bandwidth_history[-1]["download"], 2)
    }


def get_simulated_ports(mac: str) -> List[Dict[str, Any]]:
    """
    Generate simulated port scan results for a device.

    Args:
        mac: MAC address of the target device

    Returns:
        List of port dictionaries with fields:
        - port: Port number
        - protocol: 'tcp' or 'udp'
        - status: 'open', 'closed', or 'filtered'
        - service: Service name
        - risk: 'low', 'medium', or 'high'
    """
    # Find device type
    device_type = "default"
    for device in SIMULATED_DEVICES_DB:
        if device["mac"] == mac:
            device_type = device["device_type"]
            break

    # Get template
    template = PORT_SCAN_TEMPLATES.get(device_type, PORT_SCAN_TEMPLATES["default"])

    # Add some randomness (some ports may be filtered)
    results = []
    for port_info in template:
        # Randomly change status sometimes for realism
        if random.random() < 0.1:
            status = random.choice(["closed", "filtered"])
        else:
            status = port_info["status"]

        results.append({
            "port": port_info["port"],
            "protocol": port_info["protocol"],
            "status": status,
            "service": port_info["service"],
            "risk": port_info["risk"]
        })

    return results


def inject_unknown_device() -> Dict[str, Any]:
    """
    Create a fake unknown device for demo purposes.
    Used when the user clicks the demo button.

    Returns:
        Dictionary representing an unknown device
    """
    # Generate random MAC and IP
    random_mac = "DE:AD:BE:EF:%02X:%02X" % (random.randint(0, 255), random.randint(0, 255))
    random_ip = f"192.168.1.{random.randint(80, 200)}"

    unknown_names = [
        "Unknown Device", "Suspicious Device", "Unrecognized Device",
        "Alien Device", "Mystery Device", "Rogue Access Point"
    ]

    return {
        "mac": random_mac,
        "ip": random_ip,
        "name": random.choice(unknown_names),
        "category": "Unknown",
        "is_known": False,
        "status": "online",
        "is_intrusion": True  # Flag for alert system
    }


def get_bandwidth_history(limit: int = 60) -> List[Dict[str, float]]:
    """
    Get historical bandwidth data for charts.

    Args:
        limit: Maximum number of data points to return

    Returns:
        List of bandwidth data points
    """
    global _bandwidth_history

    if not _bandwidth_history:
        # Generate some initial history
        for i in range(limit):
            get_simulated_bandwidth()

    # Return last 'limit' points
    return _bandwidth_history[-limit:]


# Self-test
if __name__ == "__main__":
    print("=== SIMULATOR TEST ===")

    devices = get_simulated_devices()
    print(f"Simulated devices: {len(devices)}")
    for d in devices[:3]:
        print(f"  {d['name']} ({d['ip']}) - {d['status']}")

    bw = get_simulated_bandwidth()
    print(f"Bandwidth: ↑{bw['upload']} Mbps ↓{bw['download']} Mbps")

    unknown = inject_unknown_device()
    print(f"Injected unknown: {unknown['name']} - {unknown['ip']}")

    ports = get_simulated_ports("AA:BB:CC:DD:EE:02")
    print(f"Port scan results: {len(ports)} ports")
    for p in ports[:3]:
        print(f"  Port {p['port']}/{p['protocol']}: {p['status']} ({p['risk']} risk)")