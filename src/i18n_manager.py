# i18n_manager.py

import json
import os
from PyQt5.QtCore import QSettings

class I18nManager:
    """
    Gestiona la carga y el acceso a los archivos de traducción para la aplicación.
    """
    def __init__(self, parent=None):
        self.parent = parent
        self.settings = QSettings('Marque', 'Marque')
        self.locale = self.settings.value('locale', 'en')  # Idioma por defecto desde las settings
        self.translations = {}
        self.lang_dir = os.path.join(os.path.dirname(__file__), '..', 'res', 'lang')
        self.load_translations()

    def set_locale(self, locale):
        """
        Establece el idioma actual de la aplicación y recarga las traducciones.
        """
        if self.locale != locale:
            self.locale = locale
            self.settings.setValue('locale', locale)
            self.load_translations()
            # Esta parte se usa para notificar a la UI si es necesario
            if self.parent:
                self.parent.retranslate_ui()

    def load_translations(self):
        """
        Carga los archivos de traducción desde el directorio de idiomas.
        """
        filepath = os.path.join(self.lang_dir, f'{self.locale}.json')
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
            print(f"Traducciones para '{self.locale}' cargadas exitosamente.")
        except FileNotFoundError:
            print(f"Error: Archivo de idioma para '{self.locale}' no encontrado en '{filepath}'.")
            self.translations = {}

    def get_text(self, key):
        """
        Devuelve el texto traducido para una clave dada. Si la clave no se encuentra,
        devuelve la clave misma para evitar errores.
        """
        return self.translations.get(key, key)

    def get_available_locales(self):
        """
        Retorna una lista de los idiomas disponibles.
        """
        locales = []
        if os.path.exists(self.lang_dir):
            for filename in os.listdir(self.lang_dir):
                if filename.endswith('.json'):
                    locales.append(filename.replace('.json', ''))
        return locales
