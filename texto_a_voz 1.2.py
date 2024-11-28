#crear un programa al que proporcionarle una URL de un artículo a convertir para 
#luego manejar la conversión de texto a voz

#importar las librerias necesarias
from bs4 import BeautifulSoup
import requests
import gtts
from pydub import AudioSegment
import os
import customtkinter as ctk
from tkinter import messagebox
import re
from urllib.parse import urlparse

#definir la funcion para obtener el texto del articulo
def obtener_texto_articulo(url):
    #obtener el contenido de la pagina web
    response = requests.get(url)
    #parsear el contenido con beautifulsoup
    soup = BeautifulSoup(response.content, 'html.parser')
    #obtener el texto del articulo
    texto = soup.get_text()
    return texto    

#definir la funcion para convertir el texto a voz
def convertir_texto_a_voz(texto):
    #crear un objeto de la libreria gtts
    tts = gtts.gTTS(texto, lang='es')
    #guardar el archivo de audio
    tts.save('audio.mp3')
    #reproducir el archivo de audio
    os.system('mpg321 audio.mp3')   

class ModernTextoVoz:
    def __init__(self):
        # Configuración del tema y colores personalizados
        self.configurar_tema()
        
        # Configuración de la ventana principal
        self.root = ctk.CTk()
        self.root.title("Conversor Moderno de Texto a Voz")
        self.root.geometry("800x600")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Configuración de fuentes
        self.fuentes = {
            'titulo': ctk.CTkFont(family="Helvetica", size=28, weight="bold"),
            'subtitulo': ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            'texto': ctk.CTkFont(family="Helvetica", size=14),
            'boton': ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            'estado': ctk.CTkFont(family="Helvetica", size=12)
        }
        
        self.crear_interfaz()
        
    def configurar_tema(self):
        # Configuración de colores personalizados
        self.colores = {
            'fondo': "#2E3440",           # Azul oscuro nórdico
            'fondo_secundario': "#3B4252", # Azul grisáceo
            'texto': "#ECEFF4",           # Blanco suave
            'acento': "#88C0D0",          # Azul claro
            'error': "#BF616A",           # Rojo suave
            'exito': "#A3BE8C"            # Verde suave
        }
        
        # Aplicar tema personalizado
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

    def crear_interfaz(self):
        # Frame principal con color de fondo personalizado
        self.frame_principal = ctk.CTkFrame(
            self.root,
            fg_color=self.colores['fondo']
        )
        self.frame_principal.grid(padx=20, pady=20, sticky="nsew")
        self.frame_principal.grid_columnconfigure(0, weight=1)
        
        # Título con nueva fuente y color
        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Conversor de Texto a Voz",
            font=self.fuentes['titulo'],
            text_color=self.colores['texto']
        )
        self.titulo.grid(row=0, column=0, pady=(0, 20))
        
        self.crear_frame_url()
        self.crear_separador()
        self.crear_frame_texto()
        self.crear_barra_estado()

    def crear_frame_url(self):
        self.frame_url = ctk.CTkFrame(
            self.frame_principal,
            fg_color=self.colores['fondo_secundario']
        )
        self.frame_url.grid(row=1, column=0, sticky="ew", padx=10)
        self.frame_url.grid_columnconfigure(1, weight=1)
        
        # Etiqueta URL
        self.url_label = ctk.CTkLabel(
            self.frame_url,
            text="URL del artículo:",
            font=self.fuentes['subtitulo'],
            text_color=self.colores['texto']
        )
        self.url_label.grid(row=0, column=0, padx=10, pady=10)
        
        # Campo URL
        self.url_entry = ctk.CTkEntry(
            self.frame_url,
            placeholder_text="Ingrese la URL del artículo aquí",
            font=self.fuentes['texto'],
            height=35,
            fg_color=self.colores['fondo']
        )
        self.url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Botón URL
        self.url_button = ctk.CTkButton(
            self.frame_url,
            text="Convertir URL",
            command=self.convertir_url,
            font=self.fuentes['boton'],
            height=35,
            fg_color=self.colores['acento']
        )
        self.url_button.grid(row=0, column=2, padx=10, pady=10)

    def crear_separador(self):
        self.separador = ctk.CTkFrame(
            self.frame_principal,
            height=2,
            fg_color=self.colores['acento']
        )
        self.separador.grid(row=2, column=0, sticky="ew", pady=20)

    def crear_frame_texto(self):
        self.frame_texto = ctk.CTkFrame(
            self.frame_principal,
            fg_color=self.colores['fondo_secundario']
        )
        self.frame_texto.grid(row=3, column=0, sticky="ew", padx=10)
        self.frame_texto.grid_columnconfigure(0, weight=1)
        
        # Campo de texto
        self.texto_entry = ctk.CTkTextbox(
            self.frame_texto,
            height=200,
            font=self.fuentes['texto'],
            fg_color=self.colores['fondo']
        )
        self.texto_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Botón texto
        self.texto_button = ctk.CTkButton(
            self.frame_texto,
            text="Convertir Texto",
            command=self.convertir_texto,
            font=self.fuentes['boton'],
            height=35,
            fg_color=self.colores['acento']
        )
        self.texto_button.grid(row=1, column=0, pady=(0, 10))

    def crear_barra_estado(self):
        self.barra_estado = ctk.CTkLabel(
            self.frame_principal,
            text="Listo para convertir",
            font=self.fuentes['estado'],
            text_color=self.colores['texto']
        )
        self.barra_estado.grid(row=4, column=0, pady=(20, 0))

    def validar_url(self, url):
        """Valida el formato y accesibilidad de la URL."""
        try:
            # Validar formato de URL
            resultado = urlparse(url)
            if not all([resultado.scheme, resultado.netloc]):
                return False, "URL inválida. Asegúrese de incluir 'http://' o 'https://'"
            
            # Verificar si la URL es accesible
            response = requests.head(url, timeout=5)
            if response.status_code != 200:
                return False, f"La URL no es accesible. Código de estado: {response.status_code}"
                
            return True, "URL válida"
        except requests.RequestException as e:
            return False, f"Error al acceder a la URL: {str(e)}"

    def validar_texto(self, texto):
        """Valida el contenido del texto."""
        if not texto.strip():
            return False, "El texto no puede estar vacío"
        
        if len(texto) > self.max_caracteres:
            return False, f"El texto excede el límite de {self.max_caracteres} caracteres"
        
        # Verificar si hay caracteres válidos (no solo espacios o símbolos)
        if not re.search(r'[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ]', texto):
            return False, "El texto debe contener al menos una letra o número"
            
        return True, "Texto válido"

    def convertir_url(self):
        if self.conversion_en_progreso:
            self.actualizar_estado("Ya hay una conversión en progreso", True)
            return
            
        url = self.url_entry.get().strip()
        valido, mensaje = self.validar_url(url)
        
        if not valido:
            self.actualizar_estado(mensaje, True)
            return
            
        self.conversion_en_progreso = True
        self.url_button.configure(state="disabled")
        self.procesar_conversion(lambda: self.obtener_texto_articulo_seguro(url))

    def obtener_texto_articulo_seguro(self, url):
        try:
            # Agregar headers para evitar bloqueos
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Verificar el tipo de contenido
            if 'text/html' not in response.headers.get('Content-Type', '').lower():
                raise ValueError("La URL no contiene contenido HTML válido")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Eliminar elementos no deseados
            for elemento in soup(['script', 'style', 'head', 'header', 'footer', 'nav']):
                elemento.decompose()
            
            # Extraer texto de manera más precisa
            texto = ' '.join([p.get_text(strip=True) for p in soup.find_all(['p', 'article', 'div']) if p.get_text(strip=True)])
            
            if not texto:
                raise ValueError("No se pudo extraer texto del artículo")
            
            return texto
            
        except requests.Timeout:
            raise Exception("Tiempo de espera agotado al acceder a la URL")
        except requests.RequestException as e:
            raise Exception(f"Error al acceder a la URL: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al procesar el artículo: {str(e)}")

    def convertir_texto(self):
        if self.conversion_en_progreso:
            self.actualizar_estado("Ya hay una conversión en progreso", True)
            return
            
        texto = self.texto_entry.get("0.0", "end").strip()
        valido, mensaje = self.validar_texto(texto)
        
        if not valido:
            self.actualizar_estado(mensaje, True)
            return
            
        self.conversion_en_progreso = True
        self.texto_button.configure(state="disabled")
        self.procesar_conversion(lambda: texto)

    def procesar_conversion(self, obtener_texto):
        try:
            self.actualizar_estado("Procesando...")
            texto = obtener_texto()
            
            # Validar el texto obtenido
            valido, mensaje = self.validar_texto(texto)
            if not valido:
                raise ValueError(mensaje)
            
            # Crear directorio temporal si no existe
            temp_dir = os.path.join(os.getcwd(), 'temp_audio')
            os.makedirs(temp_dir, exist_ok=True)
            
            # Usar un nombre de archivo único con ruta completa
            archivo_audio = os.path.join(temp_dir, f'audio_{os.getpid()}.mp3')
            
            try:
                # Convertir a voz
                tts = gtts.gTTS(texto, lang='es')
                tts.save(archivo_audio)
                
                # Reproducir audio
                self.reproducir_audio(archivo_audio)
                
                self.actualizar_estado("¡Conversión completada con éxito!")
                
            except Exception as e:
                raise Exception(f"Error en la conversión: {str(e)}")
                
            finally:
                # Limpiar archivo temporal
                if os.path.exists(archivo_audio):
                    try:
                        os.remove(archivo_audio)
                    except Exception as e:
                        print(f"Error al eliminar archivo temporal: {str(e)}")
                        
        except Exception as e:
            self.actualizar_estado(f"Error: {str(e)}", True)
        finally:
            self.conversion_en_progreso = False
            self.url_button.configure(state="normal")
            self.texto_button.configure(state="normal")

    def actualizar_estado(self, mensaje, es_error=False):
        color = self.colores['error'] if es_error else self.colores['exito']
        self.barra_estado.configure(text=mensaje, text_color=color)
        
        if es_error:
            messagebox.showerror("Error", mensaje)
        elif "éxito" in mensaje.lower():
            messagebox.showinfo("Éxito", mensaje)

    def iniciar(self):
        self.root.mainloop()

    def configurar_reproductor_audio(self):
        """Verifica el sistema operativo y configura el reproductor de audio adecuado"""
        if os.name == 'nt':  # Windows
            return 'start'
        elif os.name == 'posix':  # Linux/Mac
            if os.system('which mpg321 >/dev/null 2>&1') == 0:
                return 'mpg321'
            elif os.system('which mpg123 >/dev/null 2>&1') == 0:
                return 'mpg123'
            else:
                return 'play'  # Sox player
        return None

    def reproducir_audio(self, archivo_audio):
        """Reproduce el archivo de audio de manera segura"""
        try:
            if self.audio_player:
                if os.name == 'nt':
                    os.system(f'{self.audio_player} {archivo_audio}')
                else:
                    os.system(f'{self.audio_player} "{archivo_audio}"')
            else:
                raise Exception("No se encontró un reproductor de audio compatible")
        except Exception as e:
            raise Exception(f"Error al reproducir el audio: {str(e)}")

def main():
    app = ModernTextoVoz()
    app.iniciar()

if __name__ == '__main__':
    main()


