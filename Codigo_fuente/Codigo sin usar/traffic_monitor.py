import re
import subprocess
import sys
from typing import Dict

# obtineen el trafico de la red
def get_network_traffic() -> Dict:
    traffic_info = {
        "active_connections": 0,
        "tcp_connections": 0,
        "udp_connections": 0,
        "listening_ports": 0,
        "established_connections": 0,
    }

    try:
        result = subprocess.run(
            ["netstat", "-an"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding=('mbcs' if sys.platform.startswith('win') else 'utf-8'),
            errors='ignore',
            shell=False,
            check=False,
        ).stdout or ""

        for line in result.splitlines():
            line = line.strip().upper()
            if line.startswith("TCP"):
                traffic_info["tcp_connections"] += 1
                traffic_info["active_connections"] += 1
                if "LISTENING" in line:
                    traffic_info["listening_ports"] += 1
                if "ESTABLISHED" in line:
                    traffic_info["established_connections"] += 1
            elif line.startswith("UDP"):
                traffic_info["udp_connections"] += 1
                traffic_info["active_connections"] += 1

    except Exception as exc:
        traffic_info["error"] = str(exc)

    return traffic_info
