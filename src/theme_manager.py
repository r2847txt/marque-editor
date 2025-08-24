# Lógica para cargar y aplicar temas CSS.

import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings

class ThemeManager:
    """
    Gestiona la carga, aplicación y persistencia de temas para la aplicación.
    """
    def __init__(self, parent=None):
        self.parent = parent
        self.settings = QSettings('Marque', 'Marque')
        self.themes_dir = os.path.join(os.path.dirname(__file__), '..', 'res', 'themes')
        
        # Carga el último tema usado por el usuario o usa 'dark_theme' por defecto
        self.current_theme = self.settings.value('theme', 'dark_theme')
        self.apply_theme(self.current_theme)

    def apply_theme(self, theme_name):
        """
        Aplica un tema cargando su archivo CSS y aplicándolo a la aplicación.
        """
        theme_path = os.path.join(self.themes_dir, f'{theme_name}.css')
        try:
            with open(theme_path, 'r', encoding='utf-8') as f:
                stylesheet = f.read()
                # Aplica el stylesheet a la QApplication para que afecte a todos los widgets
                QApplication.instance().setStyleSheet(stylesheet)
                # Guarda el nombre del tema para que persista al cerrar la app
                self.settings.setValue('theme', theme_name)
                self.current_theme = theme_name
                print(f"Tema '{theme_name}' aplicado.")
        except FileNotFoundError:
            print(f"Error: Archivo de tema para '{theme_name}' no encontrado en '{theme_path}'.")

    def get_available_themes(self):
        """
        Retorna una lista de los temas disponibles en el directorio de temas.
        """
        themes = []
        if os.path.exists(self.themes_dir):
            for filename in os.listdir(self.themes_dir):
                if filename.endswith('.css'):
                    themes.append(filename.replace('.css', ''))
        return themes

    def set_theme_action(self, theme_name):
        """
        Función para ser conectada a un QAction en un menú.
        """
        if self.current_theme != theme_name:
            self.apply_theme(theme_name)