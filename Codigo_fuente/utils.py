# utils.py (utilidades de escaneo, analisis y generacion de reportes)
import subprocess # import para que se puedan manejar sub procesos
import time # import para que se puedan manegar valores de tiempo
import re # import de expreciones regulares
from datetime import datetime # import de libreria para fecha
from pathlib import Path # import de libreria de caminos de archivos

from openpyxl import Workbook # import de libreria que genera el excel

# ======================================================================
# Utilidades de escaner y adaptador
# ======================================================================

# Reiniciador de el adaptador de redes
def refresh_wifi_panel():
    try:
        
        # abre el adaptador visual para que se reinicie
        subprocess.Popen(
            ["explorer.exe", "ms-availablenetworks:"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        time.sleep(3)

    except:
        pass

# Escaner de redes
def scan_wifi():
    # lista las redes en un string
    networks = []

    # intenta refrescar las redes con el metodo
    try:
        refresh_wifi_panel()

    # ecaner de red

        time.sleep(2)

        # Ejecuta el comando de sistema para obtener la lista técnica de redes cercanas
        result = subprocess.check_output(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            encoding="utf-8",
            errors="ignore"
        )

        lines = result.split("\n")
        current_network = {}

        # Itera sobre la salida de texto para estructurar la información en diccionarios
        for line in lines:
            line = line.strip()
            # Detecta el inicio de una nueva red (SSID)
            if line.startswith("SSID") and "BSSID" not in line:
                if current_network:
                    networks.append(current_network)
                    current_network = {}

                ssid = line.split(":", 1)[1].strip()

                # Maneja casos de redes que no transmiten su nombre
                if ssid == "":
                    current_network["name"] = "🔒 Red Oculta"
                    current_network["hidden"] = True
                else:
                    current_network["name"] = ssid
                    current_network["hidden"] = False

            # Extrae el tipo de autenticación (seguridad)
            elif "Authentication" in line or "Autenticación" in line:
                current_network["security"] = line.split(":", 1)[1].strip()

            # Extrae el tipo de cifrado de datos
            elif "Encryption" in line or "Cifrado" in line:
                current_network["encryption"] = line.split(":", 1)[1].strip()

            # Extrae el porcentaje de señal usando expresiones regulares
            elif "Signal" in line or "Señal" in line:
                match = re.search(r"(\d+)%", line)
                if match:
                    current_network["signal"] = int(match.group(1))
                else:
                    current_network["signal"] = None

            # Guarda la dirección física (MAC) del punto de acceso
            elif "BSSID" in line:
                bssid = line.split(":", 1)[1].strip()
                current_network.setdefault("bssid", []).append(bssid)

        # Agrega la última red procesada a la lista
        if current_network:
            networks.append(current_network)

    except Exception as e:
        print("Error escaneando redes:", e)

    return networks

# ===================================================================
# Clasificacion y analisis de redes
# ===================================================================

def classify_network(net):
    """
    Clasifica la red según su nivel de seguridad.
    """
    # Analiza las palabras clave de seguridad para determinar la vulnerabilidad
    security = net.get("security", "").upper()
    encryption = net.get("encryption", "").upper()

    # Redes sin contraseña o protocolos obsoletos
    if "OPEN" in security or "ABIERTA" in security:
        return "NO CONECTARSE"

    if "WEP" in security:
        return "NO CONECTARSE"

    # Protocolos con vulnerabilidades conocidas
    if "TKIP" in encryption:
        return "PRECAUCIÓN"

    # Estándares modernos y recomendados
    if "WPA3" in security:
        return "SEGURA (WPA3)"

    if "WPA2" in security:
        return "SEGURA"

    return "PRECAUCIÓN"

def signal_range(signal):
    """
    Convierte señal en rango aproximado.
    """
    # Estima un margen de fluctuación de la señal para el reporte
    if signal is None:
        return "N/A"

    if signal >= 80:
        return f"{signal-5}%~{signal}%"
    elif signal >= 60:
        return f"{signal-10}%~{signal}%"
    elif signal >= 40:
        return f"{signal-10}%~{signal}%"
    elif signal >= 20:
        return f"{signal-10}%~{signal}%"
    else:
        return f"{signal}%~{signal+10}%"


def detect_evil_twin(networks):
    """
    Detecta SSIDs duplicados con distinto BSSID.
    """
    # Mapea nombres de red para ver si un mismo nombre tiene múltiples direcciones físicas
    ssid_map = {}

    for net in networks:
        ssid = net.get("name")
        bssids = net.get("bssid", [])

        ssid_map.setdefault(ssid, set()).update(bssids)

    # Si un SSID tiene más de un BSSID único, se marca como sospechoso
    return [ssid for ssid, b in ssid_map.items() if len(b) > 1]


def mark_evil_twin(networks):
    """
    Marca redes sospechosas.
    """
    # Identifica cuáles nombres de red están duplicados maliciosamente
    suspicious = detect_evil_twin(networks)

    for net in networks:
        net["evil_twin"] = net.get("name") in suspicious

    return networks

def analyze_networks(networks):
   
    #Procesa redes señal, seguridad y amenazas.
    # Orquestador que aplica todas las capas de análisis a la lista de redes
    networks = mark_evil_twin(networks)

    for net in networks:
        net["classification"] = classify_network(net)
        net["signal_range"] = signal_range(net.get("signal"))

    return networks

# =================================================================
# Utilidades de generacion
# =================================================================

# Generador de archivod de reporte excel
def export_to_excel(networks):
    # Crea un nuevo libro de trabajo y establece la hoja activa
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte WiFi"

    # ===== ENCABEZADOS =====
    # Define la primera fila del documento Excel
    ws.append([
        "SSID",
        "Señal (%)",
        "Seguridad",
        "Clasificación",
        "Riesgo",
        "Evil Twin",
        "Oculta"
    ])

    # ===== DATOS =====
    # Vuelca la información de cada diccionario de red a filas de Excel
    for net in networks:
        ws.append([
            net.get("name"),
            net.get("signal"),
            net.get("security"),
            net.get("classification"),
            "Evil Twin" if net.get("evil_twin") else "Oculta" if net.get("hidden") else "Normal",
            "Sí" if net.get("evil_twin") else "No",
            "Sí" if net.get("hidden") else "No"
        ])

    # ===== NOMBRE DEL ARCHIVO Y GUARDADO=====
    # Define la ruta de almacenamiento en el disco local
    carpeta = Path("C:RedClassProyect/Reportes_wifi")
    
    # Crea la estructura de carpetas si no existe para evitar errores de guardado
    carpeta.mkdir(parents=True, exist_ok=True)
    
    # Genera un nombre único basado en la fecha y hora actual
    filename = f"reporte_wifi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    ruta_completa = carpeta / filename
    
    # Finaliza el proceso guardando el archivo físico
    wb.save(ruta_completa)

    return ruta_completa
