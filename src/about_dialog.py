# about_dialog.py

import sys
import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QApplication
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.Qt import QDesktopServices

from i18n_manager import I18nManager

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 1. Instancia del gestor de idiomas
        self.i18n = I18nManager()
        
        # 2. Traducción de la ventana
        self.setWindowTitle(self.i18n.get_text("about_dialog_title"))
        self.setFixedSize(400, 300)

        # Configurar el diseño principal
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Logotipo de Marque
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'res', 'icons', 'marque_icon.png')
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path).scaledToWidth(80, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        main_layout.addWidget(logo_label)

        # Nombre y versión
        title_label = QLabel("<h1>Marque</h1>")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 3. Traducción de la versión
        version_label = QLabel(self.i18n.get_text("version_label"))
        version_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(version_label)

        # Mensaje de créditos
        credits_label = QLabel(self.i18n.get_text("credits_message"))
        credits_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(credits_label)
        
        # Enlace a GitHub
        github_layout = QHBoxLayout()
        github_label = QLabel(self.i18n.get_text("github_label"))
        github_link = QPushButton(self.i18n.get_text("github_link"))
        github_link.setFlat(True)
        github_link.clicked.connect(self.open_github_link)

        github_layout.addWidget(github_label)
        github_layout.addWidget(github_link)
        github_layout.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(github_layout)

        # Botón de cierre
        close_button = QPushButton(self.i18n.get_text("close_button"))
        close_button.clicked.connect(self.accept)
        main_layout.addWidget(close_button)

    def open_github_link(self):
        QDesktopServices.openUrl(QUrl("https://github.com/r2847txt/marque-editor"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = AboutDialog()
    dialog.exec_()