# gui.py (interfaz grafica, diseño y representacion de datos)

# import de librerias de diseño
import tkinter as tk
from tkinter import ttk

# import de libreria de enlaces que se usan para los botones
import threading


# import de utilidades
from utils import analyze_networks, scan_wifi, export_to_excel

# clase que guarda ciertos defaults, la UI y algunas utilidades graficas
class WifiApp:

    def __init__(self, root):
        # Inicialización de la ventana principal y configuración básica
        self.root = root
        self.root.title("🐱 RedClassAnalizer")
        self.root.geometry("1000x600")

        # ===== COLORES =====
        # Definición de la paleta de colores personalizada (estilo oscuro/hacker)
        self.BG = "#000000"
        self.CARD = "#5F1525"
        self.TEXT = "#ff0000"
        self.ACCENT = "#78F752"

        self.root.configure(bg=self.BG)

        # Llamada al constructor de componentes visuales
        self.create_widgets()
        
    # =========================================================
    # HILO SCAN
    # =========================================================
    def start_scan_thread(self):
        # Ejecuta el escaneo en un hilo separado para no congelar la interfaz visual
        thread = threading.Thread(target=self.scan)
        thread.start()
    
    # ========================================================================
    # Interfaz de usuario
    # ========================================================================
    
    def create_widgets(self):
        # Contenedor principal de la interfaz
        frame = tk.Frame(self.root, bg=self.BG)
        frame.pack(fill="both", expand=True, padx=10, pady=10)  # controla márgenes

        # titulo de la pagina 
        title = tk.Label(
            frame,
            text="🐱 RedClassAnalizer",
            font=("Times New Romain", 18, "bold"),
            fg=self.ACCENT,
            bg=self.BG
        )
        title.pack(pady=10)

        # ===== BOTÓN =====
        # Botón que dispara el proceso de escaneo mediante hilos
        self.btn = tk.Button(
            frame,
            text="🔍 Escanear Redes",
            command=self.start_scan_thread,
            bg="#000000",
            fg=self.TEXT,
            relief="flat"
        )
        self.btn.pack(pady=15)
        
        # ===== Configuracion del LOADER =====
        # Etiqueta de texto para mostrar estados de carga o progreso
        self.loader_label = tk.Label(
            frame,
            text="",
            font=("Consolas", 12),
            fg=self.ACCENT,
            bg=self.BG
        )
        self.loader_label.pack(pady=5)

        # ===== ESTILO TABLA =====
        # Personalización visual de la tabla (Treeview) para que coincida con el tema
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background=self.CARD,
                        foreground=self.TEXT,
                        fieldbackground=self.CARD,
                        rowheight=28,
                        borderwidth=0)

        style.configure("Treeview.Heading",
                        background=self.BG,
                        foreground=self.ACCENT,
                        font=("Consolas", 10, "bold"))

        # ===== TABLA =====
        # Definición de columnas y encabezados para los datos de red
        columns = ("SSID", "Señal", "Seguridad", "Estado", "Riesgo")

        self.tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # ===== SCROLL TABLA =====
        # Barra de desplazamiento vertical para navegar por la lista de redes
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # ===== COLORES POR ESTADO =====
        # Mapeo de etiquetas (tags) a colores para identificar riesgos visualmente
        self.tree.tag_configure("segura", foreground="#2bff00")
        self.tree.tag_configure("precaucion", foreground="#db8007")
        self.tree.tag_configure("peligro", foreground="#910808")
        self.tree.tag_configure("no_conectar", foreground="#4b1683")

        # ===== PANEL DE REPORTE (OCULTO) =====
        # Contenedor y área de texto para mostrar logs técnicos del análisis
        self.report_frame = tk.Frame(frame, bg=self.BG)

        self.report_text = tk.Text(
            self.report_frame,
            height=8,
            bg="#000000", # no tocar, si no crashea
            fg="#1FBB00",
            insertbackground="red",
            font=("Consolas", 9),
            relief="flat"
        )

        self.report_text.pack(side="left", fill="both", expand=True)

        # Scrollbar específica para el cuadro de texto del reporte
        report_scroll = ttk.Scrollbar(self.report_frame, command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=report_scroll.set)
        report_scroll.pack(side="right", fill="y")

    # LOADER ANIMADO
    def animate_loader(self):
        # Crea una animación cíclica de caracteres en el loader_label
        frames = ["°", "°|", "°|°", "|°"]

        def loop(i=0):
            if self.loading:
                self.loader_label.config(
                    text=f"Escaneando redes... {frames[i % len(frames)]}"
                )
                self.root.after(300, loop, i + 1)

        loop()

    # SEÑAL VISUAL
    def signal_range(self, signal):
        """
        Escala más precisa (tipo Android/iOS)
        """
        # Convierte el porcentaje de señal en una barra gráfica ASCII
        try:
            signal = int(signal)
        except:
            return "|?|?|?|"

        if signal >= 90:
            return "▂▃▄▅▆▇██"   # Excelente
        elif signal >= 75:
            return "▂▃▄▅▆▇"   # Muy buena
        elif signal >= 60:
            return "▂▃▄▅▆"    # Buena
        elif signal >= 45:
            return "▂▃▄▅"    # Decente
        elif signal >= 30:
            return "▂▃▄"     # Baja
        elif signal >= 15:
            return "▂▃"     # Muy baja
        else:
            return "▂"      # Casi sin señal
            
    # =========================================================
    # Iconos de las redes
    # =========================================================
    def get_icon(self, net, clas):
        # Asigna un emoji descriptivo basado en las amenazas y la clasificación
        if net.get("evil_twin"):
            return "☠️"
        if net.get("hidden"):
            return "🔒"
        if "SEGURA" in clas:
            return "😸"
        if "PRECAUCIÓN" in clas:
            return "😺"
        if "NO CONECTARSE" in clas:
            return "🙀"
        return "😾"

    # =========================================================
    # Punto donde se converge la informacion de las redes para representarla visualmente
    # =========================================================
    def scan(self):
        # Activa el estado de carga y limpia la tabla anterior
        self.loading = True
        self.animate_loader()
        self.btn.config(state="disabled")
        
        self.tree.delete(*self.tree.get_children())

        # Configura y muestra el panel de reporte textual
        self.report_frame.pack(fill="both", padx=10, pady=5.5)
        self.report_text.delete("1.0", tk.END)
        self.report_text.insert(tk.END, "#== REPORTE DE REDES ==#\n\n")

        # Proceso principal: Escaneo -> Análisis -> Exportación
        networks = scan_wifi()
        networks = analyze_networks(networks)
        archivo = export_to_excel(networks)

        # Itera sobre las redes analizadas para procesar etiquetas y visuales
        for net in networks:

            clas = net.get("classification", "")

            # Asignación de etiquetas para aplicar los estilos de colores (tags)
            if "NO CONECTARSE" in clas:
                tag = "no_conectar"
            elif "PRECAUCIÓN" in clas:
                tag = "precaucion"
            elif "SEGURA" in clas:
                tag = "segura"
            elif "PELIGRO" in clas:
                tag = "peligro"

            # Identificación de riesgos críticos específicos
            riesgo = ""
            if net.get("evil_twin"):
                riesgo = "⚠️ Evil Twin"
            elif net.get("hidden"):
                riesgo = "🔒 Oculta"

            # Obtención de elementos visuales (iconos y barras de señal)
            icon = self.get_icon(net, clas)
            signal_visual = self.signal_range(net.get("signal", 0))
            
            # Inserción de los datos finales procesados en la tabla de la UI
            self.tree.insert(
                "",
                "end",
                values=(
                    f"{icon} {net.get('name')}",
                    signal_visual,
                    net.get("security"),
                    clas,
                    riesgo
                ),
                tags=(tag,)
            )

            # Genera el reporte en el cuadro de texto (preludio del reporte de excel)
            self.report_text.insert(tk.END, f"SSID: {net.get('name')}\n")
            self.report_text.insert(tk.END, f"Seguridad: {net.get('security')}\n")
            self.report_text.insert(tk.END, f"Clasificación: {clas}\n")
            self.report_text.insert(tk.END, "-"*30 + "\n")

        # Detiene la animación y reactiva el botón al finalizar
        self.loading = False
        self.loader_label.config(text="✅ Escaneo Finalizado")
        self.btn.config(state="normal")
