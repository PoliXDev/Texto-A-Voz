import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QTabWidget, QTextEdit, QLineEdit, 
                           QPushButton, QLabel, QProgressBar, QFileDialog, 
                           QMessageBox, QComboBox, QSlider)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor
import pyttsx3
import requests
from bs4 import BeautifulSoup

class TextToSpeechEngine:
    """Clase para manejar las operaciones del motor de texto a voz"""
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 1.0)
        except Exception as e:
            print(f"Error inicializando el motor: {e}")
            self.engine = None

    def speak(self, text, rate=150):
        """Reproduce el texto usando el motor"""
        try:
            if self.engine:
                self.engine.setProperty('rate', rate)
                self.engine.say(text)
                self.engine.runAndWait()
                return True
        except Exception as e:
            print(f"Error en speak: {e}")
        return False

    def save_to_file(self, text, filename, rate=150):
        """Guarda el texto como archivo de audio"""
        try:
            if self.engine:
                self.engine.setProperty('rate', rate)
                self.engine.save_to_file(text, filename)
                self.engine.runAndWait()
                return True
        except Exception as e:
            print(f"Error guardando archivo: {e}")
        return False

class PantallaInicio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TextoAVoz - Inicio")
        self.setFixedSize(800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E3440;
            }
            QWidget {
                background-color: #2E3440;
                color: #ECEFF4;
            }
            QPushButton {
                background-color: #5E81AC;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
                transform: scale(1.05);
            }
            QLabel {
                color: #ECEFF4;
            }
            #titulo {
                font-size: 48px;
                font-weight: bold;
                color: #88C0D0;
            }
            #subtitulo {
                font-size: 24px;
                color: #81A1C1;
            }
            #caracteristica {
                font-size: 16px;
                color: #D8DEE9;
            }
            #version {
                font-size: 14px;
                color: #4C566A;
            }
        """)
        
        self.setup_ui()
        self.center()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        # Logo o título
        titulo = QLabel("TextoAVoz")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Subtítulo
        subtitulo = QLabel("Conversor de Texto a Voz")
        subtitulo.setObjectName("subtitulo")
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo)

        # Espacio
        layout.addSpacing(30)

        # Características principales
        caracteristicas = [
            "✓ Conversión de texto a voz en español",
            "✓ Extracción de texto desde URLs",
            "✓ Control de velocidad de lectura",
            "✓ Guardado automático de archivos",
            "✓ Interfaz moderna y fácil de usar"
        ]

        for caracteristica in caracteristicas:
            label = QLabel(caracteristica)
            label.setObjectName("caracteristica")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)

        # Espacio
        layout.addSpacing(30)

        # Botón de inicio
        self.boton_inicio = QPushButton("Iniciar Programa")
        self.boton_inicio.setCursor(Qt.PointingHandCursor)
        self.boton_inicio.clicked.connect(self.iniciar_programa)
        layout.addWidget(self.boton_inicio, alignment=Qt.AlignCenter)

        # Versión y créditos
        version = QLabel("Versión 1.4 - Desarrollado por PoliXDev")
        version.setObjectName("version")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

        # Añadir stretch para centrar verticalmente
        layout.addStretch()

    def center(self):
        """Centra la ventana en la pantalla"""
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def iniciar_programa(self):
        """Inicia el programa principal"""
        self.ventana_principal = ModernTextoVoz()
        self.ventana_principal.show()
        self.close()

class ModernTextoVoz(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TextoAVoz - PoliXDev")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(800, 600)
        
        self.tts_engine = TextToSpeechEngine()
        self.ruta_guardado = os.path.join(os.path.expanduser("~"), "Documentos", "TextoAVoz")
        self.conversion_en_progreso = False
        
        os.makedirs(self.ruta_guardado, exist_ok=True)
        
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Título
        title = QLabel("TextoAVoz")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Tabs
        self.tab_widget = QTabWidget()
        
        # Tab de texto
        text_tab = QWidget()
        text_layout = QVBoxLayout(text_tab)
        self.texto_entry = QTextEdit()
        self.texto_entry.setPlaceholderText("Escribe o pega tu texto aquí...")
        self.texto_entry.setMinimumHeight(200)
        text_layout.addWidget(self.texto_entry)
        self.tab_widget.addTab(text_tab, "Texto")
        
        # Tab de URL
        url_tab = QWidget()
        url_layout = QVBoxLayout(url_tab)
        self.url_entry = QLineEdit()
        self.url_entry.setPlaceholderText("Ingresa la URL del artículo...")
        url_layout.addWidget(self.url_entry)
        
        self.url_preview = QTextEdit()
        self.url_preview.setPlaceholderText("El texto extraído aparecerá aquí...")
        self.url_preview.setReadOnly(True)
        url_layout.addWidget(self.url_preview)
        
        self.extract_button = QPushButton("Extraer Texto")
        self.extract_button.clicked.connect(self.extract_from_url)
        url_layout.addWidget(self.extract_button)
        
        self.tab_widget.addTab(url_tab, "URL")
        
        layout.addWidget(self.tab_widget)

        # Controles de velocidad
        speed_widget = QWidget()
        speed_layout = QHBoxLayout(speed_widget)
        speed_label = QLabel("Velocidad:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(50, 300)
        self.speed_slider.setValue(150)
        self.speed_value = QLabel("150")
        self.speed_slider.valueChanged.connect(
            lambda v: self.speed_value.setText(str(v))
        )
        
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_slider)
        speed_layout.addWidget(self.speed_value)
        layout.addWidget(speed_widget)

        # Botones
        buttons_layout = QHBoxLayout()
        
        self.convert_button = QPushButton("Convertir a Voz")
        self.convert_button.setMinimumHeight(50)
        self.test_button = QPushButton("Probar")
        self.credits_button = QPushButton("Créditos")
        
        buttons_layout.addWidget(self.convert_button)
        buttons_layout.addWidget(self.test_button)
        buttons_layout.addWidget(self.credits_button)
        
        layout.addLayout(buttons_layout)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)

        # Conectar señales
        self.convert_button.clicked.connect(self.start_conversion)
        self.test_button.clicked.connect(self.test_voice)
        self.credits_button.clicked.connect(self.show_credits)

    def extract_from_url(self):
        url = self.url_entry.text().strip()
        if not url:
            self.show_error("Por favor, ingresa una URL válida")
            return
            
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text() for p in paragraphs])
            self.url_preview.setText(text)
        except Exception as e:
            self.show_error(f"Error al extraer texto: {str(e)}")

    def get_current_text(self):
        if self.tab_widget.currentIndex() == 0:
            return self.texto_entry.toPlainText().strip()
        else:
            return self.url_preview.toPlainText().strip()

    def test_voice(self):
        if self.conversion_en_progreso:
            return
            
        text = self.get_current_text()
        if not text:
            self.show_error("No hay texto para probar")
            return
            
        # Usar solo las primeras 50 palabras para la prueba
        test_text = ' '.join(text.split()[:50])
        self.tts_engine.speak(test_text, self.speed_slider.value())

    def start_conversion(self):
        if self.conversion_en_progreso:
            return
            
        text = self.get_current_text()
        if not text:
            self.show_error("No hay texto para convertir")
            return
            
        self.conversion_en_progreso = True
        self.progress_bar.setMaximum(0)
        self.convert_button.setEnabled(False)
        
        self.worker = ConversionWorker(
            text,
            self.tts_engine,
            self.speed_slider.value(),
            self.ruta_guardado
        )
        self.worker.finished.connect(self.conversion_finished)
        self.worker.error.connect(self.show_error)
        self.worker.start()

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def conversion_finished(self):
        self.conversion_en_progreso = False
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(100)
        self.convert_button.setEnabled(True)
        QMessageBox.information(self, "Éxito", 
            f"Conversión completada.\nArchivo guardado en: {self.ruta_guardado}")

    def show_credits(self):
        credits_text = """
        <h2>TextoAVoz</h2>
        <p><b>Desarrollador:</b> Daniel Ruiz (PoliXDev)</p>
        <p><b>GitHub:</b> <a href="https://github.com/PoliXDev">github.com/PoliXDev</a></p>
        <p><b>Academia:</b> <a href="https://www.conquerblocks.com">ConquerBlocks</a></p>
        <p><b>Versión:</b> 1.4</p>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Créditos")
        msg.setTextFormat(Qt.RichText)
        msg.setText(credits_text)
        msg.setStyleSheet(self.styleSheet())
        msg.exec_()

    def apply_styles(self):
        """Aplica los estilos a la interfaz"""
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2E3440;
                color: #ECEFF4;
            }
            
            QTabWidget::pane {
                border: 1px solid #4C566A;
                border-radius: 5px;
                background: #3B4252;
            }
            
            QTabBar::tab {
                background: #3B4252;
                color: #ECEFF4;
                padding: 8px 20px;
                border: 1px solid #4C566A;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            
            QTabBar::tab:selected {
                background: #4C566A;
            }
            
            QTextEdit, QLineEdit {
                background-color: #3B4252;
                border: 2px solid #4C566A;
                border-radius: 5px;
                padding: 10px;
                color: #ECEFF4;
                font-size: 14px;
            }
            
            QTextEdit:focus, QLineEdit:focus {
                border: 2px solid #5E81AC;
            }
            
            QPushButton {
                background-color: #5E81AC;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background-color: #81A1C1;
            }
            
            QPushButton:pressed {
                background-color: #4C566A;
            }
            
            QPushButton:disabled {
                background-color: #4C566A;
                color: #D8DEE9;
            }
            
            QProgressBar {
                border: 2px solid #4C566A;
                border-radius: 5px;
                text-align: center;
                background-color: #3B4252;
                height: 20px;
            }
            
            QProgressBar::chunk {
                background-color: #88C0D0;
                border-radius: 3px;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #4C566A;
                height: 8px;
                background: #3B4252;
                margin: 2px 0;
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: #88C0D0;
                border: 1px solid #4C566A;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
            
            QSlider::handle:horizontal:hover {
                background: #81A1C1;
            }
            
            QLabel {
                color: #ECEFF4;
                font-size: 14px;
            }
            
            QMessageBox {
                background-color: #2E3440;
            }
            
            QMessageBox QLabel {
                color: #ECEFF4;
            }
            
            QMessageBox QPushButton {
                min-width: 80px;
            }
        """)

class ConversionWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, text, tts_engine, rate, save_path):
        super().__init__()
        self.text = text
        self.tts_engine = tts_engine
        self.rate = rate
        self.save_path = save_path
    
    def run(self):
        try:
            filename = os.path.join(
                self.save_path,
                f"audio_{len(os.listdir(self.save_path)) + 1}.mp3"
            )
            
            if self.tts_engine.save_to_file(self.text, filename, self.rate):
                self.finished.emit()
            else:
                raise Exception("Error al guardar el archivo de audio")
        except Exception as e:
            self.error.emit(str(e))

def main():
    app = QApplication(sys.argv)
    
    # Establecer estilo de fuente global
    font = QFont("Arial", 10)
    app.setFont(font)
    
    # Mostrar pantalla de inicio
    ventana_inicio = PantallaInicio()
    ventana_inicio.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


