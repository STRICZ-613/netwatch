"""
Configuration module for NetWatch backend.
Controls real vs simulation mode and network scanning parameters.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# ============================================================================
# CORE CONFIGURATION
# ============================================================================

# Set to True for real network scanning (requires scapy + admin privileges)
# Set to False for demo mode with simulated data
USE_REAL_SCANNER: bool = os.getenv("USE_REAL_SCANNER", "False").lower() == "true"

# Network range to scan (CIDR notation)
# Examples: "192.168.1.0/24", "10.0.0.0/24", "172.16.0.0/16"
NETWORK_RANGE: str = os.getenv("NETWORK_RANGE", "192.168.1.0/24")

# How often to scan the network (in seconds)
SCAN_INTERVAL: int = int(os.getenv("SCAN_INTERVAL", "5"))

# WebSocket broadcast settings
WS_BROADCAST_INTERVAL: int = int(os.getenv("WS_BROADCAST_INTERVAL", "2"))

# ============================================================================
# SIMULATED DATA CONFIGURATION
# ============================================================================

# Number of simulated devices to generate
SIMULATED_DEVICE_COUNT: int = int(os.getenv("SIMULATED_DEVICE_COUNT", "12"))

# Bandwidth simulation range (Mbps)
SIMULATED_BANDWIDTH_MIN: float = 0.5
SIMULATED_BANDWIDTH_MAX: float = 25.0

# ============================================================================
# REAL SCANNER CONFIGURATION
# ============================================================================

# ARP scan timeout (seconds)
ARP_SCAN_TIMEOUT: int = int(os.getenv("ARP_SCAN_TIMEOUT", "3"))

# Network interface to monitor for bandwidth (None = auto-detect)
NETWORK_INTERFACE: str | None = os.getenv("NETWORK_INTERFACE", None)

# ============================================================================
# VALIDATION
# ============================================================================

def validate_config() -> dict:
    """
    Validate configuration and return status.
    Called at startup to warn about potential issues.
    """
    warnings = []
    errors = []
    
    if USE_REAL_SCANNER:
        try:
            import scapy.all  # noqa
        except ImportError:
            errors.append("scapy not installed. Run: pip install scapy")
        
        try:
            import psutil  # noqa
        except ImportError:
            errors.append("psutil not installed. Run: pip install psutil")
        
        warnings.append("REAL SCANNER MODE: Requires admin/root privileges")
    
    # Validate network range format
    if "/" not in NETWORK_RANGE:
        errors.append(f"Invalid NETWORK_RANGE format: {NETWORK_RANGE}. Expected CIDR (e.g., 192.168.1.0/24)")
    
    return {
        "valid": len(errors) == 0,
        "warnings": warnings,
        "errors": errors,
        "mode": "REAL" if USE_REAL_SCANNER else "SIMULATED",
        "network_range": NETWORK_RANGE,
        "scan_interval": SCAN_INTERVAL
    }

if __name__ == "__main__":
    # Quick test
    print(validate_config())