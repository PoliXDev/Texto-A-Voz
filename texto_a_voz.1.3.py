# Texto a Voz 1.3 - por Daniel Ruiz Poli aka NoahKnox

import customtkinter as ctk
from bs4 import BeautifulSoup
import requests
import gtts
import os
from tkinter import messagebox
import re
from urllib.parse import urlparse
from tkinter import filedialog
import time

class ModernTextoVoz:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Conversor de Texto a Voz - por PoliXDev")
        self.root.geometry("800x600")
        
        # Variables de control
        self.ruta_guardado = os.path.join(os.path.expanduser("~"), "Documentos", "TextoAVoz")
        self.conversion_en_progreso = False
        
        # Configurar tema y colores
        self.colores = {
            'fondo': "#2E3440",
            'fondo_secundario': "#3B4252",
            'texto': "#ECEFF4",
            'acento': "#88C0D0",
            'boton': "#5E81AC",
            'destacado': "#A3BE8C",
            'error': "#BF616A"
        }
        
        # Configurar fuentes
        self.fuentes = {
            'titulo': ctk.CTkFont(family="Arial", size=28, weight="bold"),
            'texto': ctk.CTkFont(family="Arial", size=14),
            'boton': ctk.CTkFont(family="Arial", size=14, weight="bold"),
            'estado': ctk.CTkFont(family="Arial", size=12)
        }
        
        self.configurar_estilos()
        self.crear_interfaz()
        
    def configurar_estilos(self):
        """Configura colores y fuentes de la aplicación"""
        # Configuración de tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Colores
        self.colores = {
            'fondo': "#2E3440",
            'fondo_secundario': "#3B4252",
            'texto': "#ECEFF4",
            'acento': "#88C0D0",
            'boton': "#5E81AC",
            'destacado': "#A3BE8C",
            'error': "#BF616A",
            'titulo_gradiente': "#81A1C1"
        }
        
        # Fuentes
        self.fuentes = {
            'titulo_grande': ctk.CTkFont(family="Arial", size=52, weight="bold"),
            'titulo': ctk.CTkFont(family="Arial", size=32, weight="bold"),
            'subtitulo': ctk.CTkFont(family="Arial", size=24),
            'boton': ctk.CTkFont(family="Arial", size=18, weight="bold"),
            'texto': ctk.CTkFont(family="Arial", size=16),
            'caracteristicas': ctk.CTkFont(family="Arial", size=15),
            'creditos': ctk.CTkFont(family="Arial", size=14),
            'version': ctk.CTkFont(family="Arial", size=12, weight="bold")
        }

    def crear_interfaz(self):
        # Frame principal
        self.frame_principal = ctk.CTkFrame(
            self.root,
            fg_color=self.colores['fondo']
        )
        self.frame_principal.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Título
        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Conversor de Texto a Voz",
            font=self.fuentes['titulo'],
            text_color=self.colores['texto']
        )
        self.titulo.pack(pady=20)
        
        # Frame para pestañas
        self.tab_view = ctk.CTkTabview(
            self.frame_principal,
            fg_color=self.colores['fondo_secundario']
        )
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.tab_texto = self.tab_view.add("Texto")
        self.tab_url = self.tab_view.add("URL")
        
        # Contenido pestaña texto
        self.texto_entry = ctk.CTkTextbox(
            self.tab_texto,
            height=200,
            font=self.fuentes['texto'],
            fg_color=self.colores['fondo']
        )
        self.texto_entry.pack(fill="x", padx=20, pady=20)
        
        # Contenido pestaña URL
        self.url_entry = ctk.CTkEntry(
            self.tab_url,
            font=self.fuentes['texto'],
            fg_color=self.colores['fondo'],
            placeholder_text="Ingrese la URL del artículo"
        )
        self.url_entry.pack(fill="x", padx=20, pady=20)
        
        # Frame para botones
        self.frame_botones = ctk.CTkFrame(
            self.frame_principal,
            fg_color="transparent"
        )
        self.frame_botones.pack(fill="x", padx=20, pady=10)
        
        # Botones
        self.boton_convertir = ctk.CTkButton(
            self.frame_botones,
            text="Convertir a Voz",
            command=self.iniciar_conversion,
            font=self.fuentes['boton'],
            fg_color=self.colores['boton'],
            hover_color=self.colores['acento']
        )
        self.boton_convertir.pack(side="left", padx=5)
        
        self.boton_ruta = ctk.CTkButton(
            self.frame_botones,
            text="Cambiar Ruta",
            command=self.cambiar_ruta,
            font=self.fuentes['boton'],
            fg_color=self.colores['boton'],
            hover_color=self.colores['acento']
        )
        self.boton_ruta.pack(side="left", padx=5)
        
        self.boton_salir = ctk.CTkButton(
            self.frame_botones,
            text="Salir",
            command=self.confirmar_salida,
            font=self.fuentes['boton'],
            fg_color=self.colores['error'],
            hover_color=self.colores['acento']
        )
        self.boton_salir.pack(side="right", padx=5)
        
        # Frame para estado y progreso
        self.frame_estado = ctk.CTkFrame(
            self.frame_principal,
            fg_color="transparent"
        )
        self.frame_estado.pack(fill="x", padx=20, pady=10)

        # Barra de progreso
        self.progreso = ctk.CTkProgressBar(
            self.frame_estado,
            mode="indeterminate",
            fg_color=self.colores['fondo_secundario'],
            progress_color=self.colores['acento']
        )
        self.progreso.pack(fill="x", pady=(0, 5))
        self.progreso.set(0)

        # Estado
        self.estado = ctk.CTkLabel(
            self.frame_estado,
            text="Listo para convertir",
            font=self.fuentes['estado'],
            text_color=self.colores['texto']
        )
        self.estado.pack(pady=5)

        # Ruta actual
        self.label_ruta = ctk.CTkLabel(
            self.frame_estado,
            text=f"Ruta de guardado: {self.ruta_guardado}",
            font=self.fuentes['estado'],
            text_color=self.colores['texto']
        )
        self.label_ruta.pack(pady=5)

        # Información academia
        self.info_academia = ctk.CTkLabel(
            self.frame_principal,
            text="Academia ConquerBlocks - Noviembre 2024",
            font=self.fuentes['estado'],
            text_color=self.colores['destacado']
        )
        self.info_academia.pack(side="bottom", pady=10)

    def iniciar_conversion(self):
        if self.conversion_en_progreso:
            return
            
        self.conversion_en_progreso = True
        self.progreso.start()
        self.boton_convertir.configure(state="disabled")
        
        try:
            if self.tab_view.get() == "Texto":
                texto = self.texto_entry.get("1.0", "end-1c")
                if not texto.strip():
                    raise ValueError("Por favor, ingrese texto para convertir")
            else:
                url = self.url_entry.get().strip()
                if not url:
                    raise ValueError("Por favor, ingrese una URL válida")
                self.actualizar_estado("Extrayendo texto de la URL...")
                texto = self.extraer_texto_url(url)
            
            self.actualizar_estado("Convirtiendo texto a voz...")
            self.convertir_a_voz(texto)
            
        except Exception as e:
            self.actualizar_estado(f"Error: {str(e)}", True)
        finally:
            self.conversion_en_progreso = False
            self.progreso.stop()
            self.progreso.set(0)
            self.boton_convertir.configure(state="normal")

    def extraer_texto_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Eliminar scripts y estilos
        for script in soup(["script", "style"]):
            script.decompose()
        texto = soup.get_text()
        # Limpiar texto
        lines = (line.strip() for line in texto.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        texto = ' '.join(chunk for chunk in chunks if chunk)
        return texto

    def convertir_a_voz(self, texto):
        try:
            # Crear directorio si no existe
            os.makedirs(self.ruta_guardado, exist_ok=True)
            
            # Generar nombre de archivo único
            nombre_archivo = f"audio_{int(time.time())}.mp3"
            ruta_completa = os.path.join(self.ruta_guardado, nombre_archivo)
            
            # Convertir y guardar
            tts = gtts.gTTS(texto, lang='es')
            tts.save(ruta_completa)
            
            # Reproducir
            if os.name == 'nt':
                os.system(f'start "{ruta_completa}"')
            else:
                os.system(f'mpg123 "{ruta_completa}"')
                
            self.actualizar_estado(f"¡Conversión completada! Archivo guardado en: {ruta_completa}")
            
        except Exception as e:
            raise Exception(f"Error en la conversión: {str(e)}")

    def cambiar_ruta(self):
        nueva_ruta = filedialog.askdirectory(
            title="Seleccionar carpeta de guardado",
            initialdir=self.ruta_guardado
        )
        if nueva_ruta:
            self.ruta_guardado = nueva_ruta
            self.label_ruta.configure(text=f"Ruta de guardado: {self.ruta_guardado}")
            self.actualizar_estado("Ruta de guardado actualizada")

    def confirmar_salida(self):
        if messagebox.askokcancel("Salir", "¿Desea salir del programa?"):
            self.root.quit()

    def actualizar_estado(self, mensaje, es_error=False):
        """Actualiza el mensaje de estado y su color"""
        try:
            color = self.colores['error'] if es_error else self.colores['texto']
            self.estado.configure(text=mensaje, text_color=color)
            # Actualizar la interfaz inmediatamente
            self.root.update()
        except Exception as e:
            print(f"Error al actualizar estado: {str(e)}")

    def iniciar(self):
        self.root.mainloop()

class PantallaInicio:
    def __init__(self):
        # Inicialización de la ventana
        self.ventana = ctk.CTk()
        self.ventana.title("Texto a Voz - por PoliXDev")
        self.ventana.geometry("1000x600")
        self.ventana.resizable(False, False)
        
        # Configurar tema y colores
        self.configurar_estilos()
        
        # Crear interfaz
        self.crear_interfaz()
        
    def configurar_estilos(self):
        """Configura colores y fuentes de la aplicación"""
        # Configuración de tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Colores
        self.colores = {
            'fondo': "#2E3440",
            'fondo_secundario': "#3B4252",
            'texto': "#ECEFF4",
            'acento': "#88C0D0",
            'boton': "#5E81AC",
            'destacado': "#A3BE8C",
            'error': "#BF616A",
            'titulo_gradiente': "#81A1C1"
        }
        
        # Fuentes
        self.fuentes = {
            'titulo_grande': ctk.CTkFont(family="Arial", size=52, weight="bold"),
            'titulo': ctk.CTkFont(family="Arial", size=32, weight="bold"),
            'subtitulo': ctk.CTkFont(family="Arial", size=24),
            'boton': ctk.CTkFont(family="Arial", size=18, weight="bold"),
            'texto': ctk.CTkFont(family="Arial", size=16),
            'caracteristicas': ctk.CTkFont(family="Arial", size=15),
            'creditos': ctk.CTkFont(family="Arial", size=14),
            'version': ctk.CTkFont(family="Arial", size=12, weight="bold")
        }

    def crear_interfaz(self):
        # Frame principal
        self.frame_principal = ctk.CTkFrame(
            self.ventana,
            fg_color=self.colores['fondo']
        )
        self.frame_principal.pack(expand=True, fill="both")
        
        # Frame izquierdo (40%)
        self.frame_izquierdo = ctk.CTkFrame(
            self.frame_principal,
            fg_color=self.colores['fondo_secundario']
        )
        self.frame_izquierdo.pack(side="left", fill="y", padx=20, pady=20)
        
        # Frame derecho (60%)
        self.frame_derecho = ctk.CTkFrame(
            self.frame_principal,
            fg_color=self.colores['fondo_secundario']
        )
        self.frame_derecho.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.crear_seccion_izquierda()
        self.crear_seccion_derecha()

    def crear_seccion_izquierda(self):
        # Título
        self.titulo = ctk.CTkLabel(
            self.frame_izquierdo,
            text="TEXTO\nA VOZ",
            font=self.fuentes['titulo_grande'],
            text_color=self.colores['texto']
        )
        self.titulo.pack(pady=(50, 20))
        
        # Versión
        self.version = ctk.CTkLabel(
            self.frame_izquierdo,
            text="⚡ Versión 1.3.0 ⚡",
            font=self.fuentes['version'],
            text_color=self.colores['acento']
        )
        self.version.pack(pady=(0, 40))
        
        # Botones
        self.boton_iniciar = ctk.CTkButton(
            self.frame_izquierdo,
            text="▶ Iniciar Programa",
            command=self.iniciar_aplicacion,
            font=self.fuentes['boton'],
            fg_color=self.colores['boton'],
            hover_color=self.colores['acento'],
            width=200,
            height=50
        )
        self.boton_iniciar.pack(pady=10)
        
        self.boton_salir = ctk.CTkButton(
            self.frame_izquierdo,
            text="✖ Salir",
            command=self.ventana.quit,
            font=self.fuentes['boton'],
            fg_color=self.colores['error'],
            hover_color=self.colores['acento'],
            width=200,
            height=50
        )
        self.boton_salir.pack(pady=10)
        
        # Frame para información del desarrollador
        self.dev_frame = ctk.CTkFrame(
            self.frame_izquierdo,
            fg_color="transparent"
        )
        self.dev_frame.pack(side="bottom", pady=20)
        
        # Etiqueta "Desarrollado por"
        self.dev_label = ctk.CTkLabel(
            self.dev_frame,
            text="Desarrollado por:",
            font=self.fuentes['creditos'],
            text_color=self.colores['texto']
        )
        self.dev_label.pack(pady=(0, 5))
        
        # Nombre del desarrollador 
        self.dev_name = ctk.CTkLabel(
            self.dev_frame,
            text="Daniel Ruiz Poli",
            font=self.fuentes['subtitulo'],
            text_color=self.colores['destacado']
        )
        self.dev_name.pack(pady=(0, 5))
        
        # GitHub
        self.github = ctk.CTkLabel(
            self.dev_frame,
            text="GitHub: PoliXDev",
            font=self.fuentes['creditos'],
            text_color=self.colores['acento']
        )
        self.github.pack()

    def crear_seccion_derecha(self):
        # Título de características
        self.caracteristicas_titulo = ctk.CTkLabel(
            self.frame_derecho,
            text="Características",
            font=self.fuentes['titulo'],
            text_color=self.colores['acento']
        )
        self.caracteristicas_titulo.pack(pady=(40, 20))
        
        # Lista de características simplificada
        caracteristicas = [
            ("►", "Conversión de texto a voz en español"),
            ("→", "Soporte para URLs y texto directo"),
            ("□", "Interfaz moderna y fácil de usar"),
            ("■", "Control de errores avanzado"),
            ("♪", "Reproducción de audio integrada"),
            ("✎", "Sin límite de caracteres")
        ]
        
        # Frame para características
        self.frame_caracteristicas = ctk.CTkFrame(
            self.frame_derecho,
            fg_color="transparent"
        )
        self.frame_caracteristicas.pack(fill="x", padx=20)
        
        # Crear cada característica
        for icono, texto in caracteristicas:
            frame_item = ctk.CTkFrame(
                self.frame_caracteristicas,
                fg_color="transparent"
            )
            frame_item.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                frame_item,
                text=f"{icono}  {texto}",
                font=self.fuentes['caracteristicas'],
                text_color=self.colores['texto'],
                anchor="w"
            ).pack(fill="x", padx=20)
        
        # Frame inferior
        self.frame_inferior = ctk.CTkFrame(
            self.frame_derecho,
            fg_color="transparent"
        )
        self.frame_inferior.pack(side="bottom", fill="x", pady=20)
        
        # Academia
        self.academia = ctk.CTkLabel(
            self.frame_inferior,
            text="Academia ConquerBlocks",
            font=self.fuentes['texto'],
            text_color=self.colores['destacado']
        )
        self.academia.pack(side="left", padx=20)
        
        # Fecha
        self.fecha = ctk.CTkLabel(
            self.frame_inferior,
            text="Noviembre 2024",
            font=self.fuentes['texto'],
            text_color=self.colores['texto']
        )
        self.fecha.pack(side="right", padx=20)

    def iniciar_aplicacion(self):
        self.ventana.destroy()
        app = ModernTextoVoz()
        app.iniciar()

    def iniciar(self):
        self.ventana.mainloop()

def main():
    app = PantallaInicio()
    app.iniciar()

if __name__ == '__main__':
    main()


