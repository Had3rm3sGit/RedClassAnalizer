# info.py (informacion de la red, detalles de conexion y seguridad) |actualmente en desuso|

#===========================================
#Se encarga de Dar la informacion de la red, cosas tales como el tipo de seguridad, 
#===========================================
import re
import socket
import subprocess
import sys
from typing import Dict

# preferencia de codificacion en formato de cadena
# Determina la codificación adecuada según el sistema operativo (Windows usa 'mbcs')
def _preferred_encoding() -> str:
    return 'mbcs' if sys.platform.startswith('win') else 'utf-8'

# inicia processos solicitados y regresa errores si es que detecta alguno
# Ejecuta comandos de sistema de forma segura y captura la salida de texto
def _run(command: list[str]) -> str:
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding=_preferred_encoding(),
        errors='ignore',
        shell=False,
        check=False,
    )
    return completed.stdout or ""

# extae ciertos valores que se le solicitan
# Limpia y separa el contenido de una línea después del carácter de dos puntos
def _extract_value(line: str) -> str:
    return line.split(":", 1)[1].strip() if ":" in line else ""

# se encarga de obtener la informacion de la red
def get_network_info() -> Dict:
    # Estructura base para almacenar los datos de la conexión actual
    info: Dict = {
        "hostname": "Desconocido",
        "ip": "No detectada",
        "ssid": "No conectado",
        "signal": "?",
        "security": "?",
        "gateway": "No detectado",
    }

    # Intenta obtener el nombre del equipo en la red local
    try:
        info["hostname"] = socket.gethostname() or "Desconocido"
    except Exception:
        pass

    # Identifica mejor la IPv4
    # Resuelve la dirección IP asociada al nombre del equipo, omitiendo el localhost
    try:
        host_ip = socket.gethostbyname(info["hostname"])
        if host_ip and host_ip != "127.0.0.1":
            info["ip"] = host_ip
    except Exception:
        pass

    # Obtiene detalles específicos de la interfaz inalámbrica activa
    try:
        result = _run(["netsh", "wlan", "show", "interfaces"])
        for line in result.splitlines():
            line = line.strip()
            lower = line.lower()
            
            # Extrae el nombre de la red (SSID) evitando confundirse con el BSSID
            if lower.startswith("ssid") and "bssid" not in lower:
                value = _extract_value(line)
                if value:
                    info["ssid"] = value
            # Captura la potencia de la señal actual
            elif "signal" in lower or "señal" in lower:
                value = _extract_value(line)
                if value:
                    info["signal"] = value
            # Identifica el método de autenticación/seguridad de la red
            elif "authentication" in lower or "autenticación" in lower or "autenticacion" in lower:
                value = _extract_value(line)
                if value:
                    info["security"] = value
    except Exception:
        pass

    # Busca la dirección de la puerta de enlace (Gateway) del router
    try:
        result = _run(["ipconfig"])
        # Expresión regular para detectar la puerta de enlace en español o inglés
        gateway_regex = re.compile(r"(Default Gateway|Puerta de enlace predeterminada)\s*.*:\s*(.*)$", re.IGNORECASE)
        for line in result.splitlines():
            match = gateway_regex.search(line)
            if match:
                gateway = match.group(2).strip()
                if gateway:
                    info["gateway"] = gateway
                    break
    except Exception:
        pass

    return info
