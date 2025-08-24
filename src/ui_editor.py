# Clase principal de la ventana y la UI.# ui_editor.py

import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QSplitter, QTextEdit, QVBoxLayout,
    QFileSystemModel, QTreeView, QApplication
)
from PyQt5.QtCore import Qt, QTimer, QDir
from PyQt5.QtGui import QIcon, QFont

import markdown
import os

class MarqueEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuración inicial de la ventana
        self.setWindowTitle("Marque")
        # Asegúrate de tener un icono en la ruta res/icons/marque_icon.png
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'res', 'icons', 'marque_icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(100, 100, 1200, 800)

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        """
        Configura la interfaz de usuario con un diseño de tres paneles.
        """
        # Widget central que contiene el QSplitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # QSplitter para los tres paneles
        self.splitter = QSplitter(Qt.Horizontal)
        
        # Panel 1: Gestor de Archivos
        self.file_manager_widget = QTreeView()
        self.file_manager_widget.setAccessibleName("Gestor de archivos")
        self.setup_file_manager()
        self.splitter.addWidget(self.file_manager_widget)

        # Panel 2: Editor de Markdown
        self.editor = QTextEdit()
        self.editor.setAccessibleName("Editor de Markdown")
        self.editor.setFont(QFont("Monospace", 10))
        self.splitter.addWidget(self.editor)

        # Panel 3: Previsualización HTML
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setAccessibleName("Previsualización de documento")
        self.splitter.addWidget(self.preview)

        # Establecer las proporciones iniciales de los paneles (20%, 40%, 40%)
        self.splitter.setSizes([200, 400, 400])

        # Agregar el splitter al layout principal del widget central
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(self.splitter)

    def setup_file_manager(self):
        """
        Configura el modelo del sistema de archivos para el gestor de archivos.
        """
        self.file_model = QFileSystemModel()
        # Define la carpeta de inicio para la navegación
        self.file_model.setRootPath(QDir.homePath())
        self.file_manager_widget.setModel(self.file_model)
        self.file_manager_widget.setRootIndex(self.file_model.index(QDir.homePath()))
        
        # Ocultar columnas que no son necesarias
        self.file_manager_widget.setColumnHidden(1, True) # Tamaño
        self.file_manager_widget.setColumnHidden(2, True) # Tipo
        self.file_manager_widget.setColumnHidden(3, True) # Fecha

    def setup_connections(self):
        """
        Establece las conexiones para la previsualización en tiempo real.
        """
        # Conexión del editor para la previsualización
        self.editor.textChanged.connect(self.update_preview)

    def update_preview(self):
        """
        Convierte el texto del editor a HTML y actualiza la previsualización.
        """
        markdown_text = self.editor.toPlainText()
        # Usamos la librería 'markdown' para convertir el texto
        html_output = markdown.markdown(markdown_text)
        self.preview.setHtml(html_output)

    def open_file(self, file_path):
        """
        Abre un archivo y carga su contenido en el editor.
        """
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.editor.setPlainText(f.read())
                self.setWindowTitle(f"Marque - {os.path.basename(file_path)}")
                self.current_file = file_path
            except Exception as e:
                print(f"Error al abrir el archivo: {e}")

if __name__ == '__main__':
    # Esto solo se ejecuta si corres este archivo directamente
    app = QApplication(sys.argv)
    editor = MarqueEditor()
    editor.show()
    sys.exit(app.exec_())