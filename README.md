Esta aplicación combina una interfaz moderna con funcionalidades robustas para la conversión de texto a voz, ofreciendo una experiencia de usuario completa y profesional.


# Control de Progreso:
Barra de progreso indeterminada
Bloqueo de botones durante la conversión
Indicadores visuales de estado
Gestión de Archivos:
Nombres únicos basados en timestamp
Organización en carpetas
Rutas personalizables
Interfaz Responsiva:
Adaptación a diferentes tamaños
Feedback visual inmediato
Mensajes de estado claros
Seguridad:
Validación de entradas
Manejo de errores robusto
Confirmación de salida

# Dependencias necesarias
import customtkinter as ctk
from bs4 import BeautifulSoup
import requests
import gtts
import os
from tkinter import messagebox, filedialog
import time

# Conversión de Texto:
Ingresar texto directamente
O pegar una URL
Seleccionar carpeta de destino (opcional)
Clic en "Convertir"
Resultados:
Archivo MP3 generado
Reproducción automática
Mensaje de confirmación

desarrollado por PoliXDev
Daniel Ruiz Poli
danielruizpoli@gmail.com
Estudiante academia conquerblocks
