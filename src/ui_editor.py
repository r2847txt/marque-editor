# ui_editor.py

import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QSplitter, QTextEdit, QVBoxLayout,
    QFileSystemModel, QTreeView, QApplication, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, QDir
from PyQt5.QtGui import QIcon, QFont

from theme_manager import ThemeManager

import markdown
import os

class MarqueEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Estado de la aplicación
        self.current_file = None  # Almacena la ruta del archivo actual
        self.theme_manager = ThemeManager(self)
        # Configuración inicial de la ventana
        self.setWindowTitle("Marque - Sin Título")
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'res', 'icons', 'marque_icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(100, 100, 1200, 800)

        self.setup_ui()
        self.setup_connections()
        self.create_menus()

    def setup_ui(self):
        """
        Configura la interfaz de usuario con un diseño de tres paneles.
        """
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
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

        self.splitter.setSizes([200, 400, 400])

        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(self.splitter)

    def setup_file_manager(self):
        """
        Configura el modelo del sistema de archivos para el gestor de archivos.
        """
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.homePath())
        self.file_manager_widget.setModel(self.file_model)
        self.file_manager_widget.setRootIndex(self.file_model.index(QDir.homePath()))
        
        self.file_manager_widget.setColumnHidden(1, True)
        self.file_manager_widget.setColumnHidden(2, True)
        self.file_manager_widget.setColumnHidden(3, True)

    def setup_connections(self):
        """
        Establece las conexiones para la previsualización y el gestor de archivos.
        """
        self.editor.textChanged.connect(self.update_preview)
        # Conecta el doble clic en el gestor de archivos a la función open_file
        self.file_manager_widget.doubleClicked.connect(self.open_selected_file)

    def create_menus(self):
        """
        Crea la barra de menú con las opciones de archivo.
        """
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Archivo")

        open_action = file_menu.addAction("Abrir...")
        open_action.triggered.connect(self.open_file_dialog)

        save_action = file_menu.addAction("Guardar")
        save_action.triggered.connect(self.save_file)

        save_as_action = file_menu.addAction("Guardar como...")
        save_as_action.triggered.connect(self.save_file_as)

        # Acciones para el menú Temas
        theme_menu = menu_bar.addMenu("Temas")
        themes = self.theme_manager.get_available_themes()
        for theme_name in themes:
            action = theme_menu.addAction(theme_name.replace('_', ' ').title())
            action.triggered.connect(lambda _, name=theme_name: self.theme_manager.set_theme_action(name))

  

    def open_selected_file(self, index):
        """
        Abre el archivo seleccionado en el gestor de archivos.
        """
        file_path = self.file_model.filePath(index)
        if os.path.isfile(file_path):
            self.open_file(file_path)

    def open_file_dialog(self):
        """
        Muestra un cuadro de diálogo para abrir un archivo.
        """
        # Cuadro de diálogo para seleccionar archivos Markdown
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir archivo", "", "Archivos Markdown (*.md);;Todos los archivos (*)")
        if file_path:
            self.open_file(file_path)

    def open_file(self, file_path):
        """
        Carga el contenido de un archivo en el editor.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.editor.setPlainText(f.read())
            self.current_file = file_path
            self.setWindowTitle(f"Marque - {os.path.basename(file_path)}")
        except Exception as e:
            QMessageBox.warning(self, "Error al abrir", f"No se pudo abrir el archivo:\n{e}")

    def save_file(self):
        """
        Guarda el archivo actual. Si no hay un archivo, llama a save_file_as().
        """
        if self.current_file:
            self.save_to_path(self.current_file)
        else:
            self.save_file_as()

    def save_file_as(self):
        """
        Muestra un cuadro de diálogo para guardar un archivo por primera vez.
        """
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "", "Archivos Markdown (*.md);;Todos los archivos (*)")
        if file_path:
            # Asegura la extensión .md si no fue incluida
            if not file_path.endswith('.md'):
                file_path += '.md'
            self.save_to_path(file_path)

    def save_to_path(self, file_path):
        """
        Guarda el contenido del editor en la ruta especificada.
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            self.current_file = file_path
            self.setWindowTitle(f"Marque - {os.path.basename(file_path)}")
        except Exception as e:
            QMessageBox.warning(self, "Error al guardar", f"No se pudo guardar el archivo:\n{e}")

    def update_preview(self):
        """
        Convierte el texto del editor a HTML y actualiza la previsualización.
        """
        markdown_text = self.editor.toPlainText()
        html_output = markdown.markdown(markdown_text)
        self.preview.setHtml(html_output)

if __name__ == '__main__':
    # Esto solo se ejecuta si corres este archivo directamente
    app = QApplication(sys.argv)
    editor = MarqueEditor()
    editor.show()
    sys.exit(app.exec_())