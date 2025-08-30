# ui_editor.py

import sys
import os
import markdown
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QSplitter, QTextEdit, QVBoxLayout,
    QFileSystemModel, QTreeView, QApplication, QFileDialog, QMessageBox, QAction
)
from PyQt5.QtCore import Qt, QDir, QSettings, QCoreApplication
from PyQt5.QtGui import QIcon, QFont

from theme_manager import ThemeManager
from i18n_manager import I18nManager

class MarqueEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.settings = QSettings('Marque', 'Marque')
        
        # 1. Instanciar el gestor de idiomas y cargar el idioma guardado
        self.i18n = I18nManager()
        self.i18n.set_locale(self.settings.value('locale', 'en'))

        self.theme_manager = ThemeManager(self)
        
        self.current_file = None
        
        self.setWindowTitle(self.i18n.get_text("untitled_document"))
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'res', 'icons', 'marque_icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(100, 100, 1200, 800)

        self.setup_ui()
        self.setup_connections()
        self.create_menus()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.splitter = QSplitter(Qt.Horizontal)
        
        self.file_manager_widget = QTreeView()
        self.file_manager_widget.setAccessibleName(self.i18n.get_text("file_manager_accessible_name"))
        self.setup_file_manager()
        self.splitter.addWidget(self.file_manager_widget)

        self.editor = QTextEdit()
        self.editor.setAccessibleName(self.i18n.get_text("editor_accessible_name"))
        self.editor.setFont(QFont("Monospace", 10))
        self.splitter.addWidget(self.editor)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setAccessibleName(self.i18n.get_text("preview_accessible_name"))
        self.splitter.addWidget(self.preview)

        self.splitter.setSizes([200, 400, 400])

        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(self.splitter)

    def setup_file_manager(self):
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.homePath())
        self.file_manager_widget.setModel(self.file_model)
        self.file_manager_widget.setRootIndex(self.file_model.index(QDir.homePath()))
        
        self.file_manager_widget.setColumnHidden(1, True)
        self.file_manager_widget.setColumnHidden(2, True)
        self.file_manager_widget.setColumnHidden(3, True)

    def setup_connections(self):
        self.editor.textChanged.connect(self.update_preview)
        self.file_manager_widget.doubleClicked.connect(self.open_selected_file)

    def create_menus(self):
        menu_bar = self.menuBar()
        
        # Menú Archivo
        file_menu = menu_bar.addMenu(self.i18n.get_text("file_menu"))
        open_action = file_menu.addAction(self.i18n.get_text("open_action"))
        open_action.triggered.connect(self.open_file_dialog)
        save_action = file_menu.addAction(self.i18n.get_text("save_action"))
        save_action.triggered.connect(self.save_file)
        save_as_action = file_menu.addAction(self.i18n.get_text("save_as_action"))
        save_as_action.triggered.connect(self.save_file_as)

        # Menú Temas
        theme_menu = menu_bar.addMenu(self.i18n.get_text("theme_menu"))
        themes = self.theme_manager.get_available_themes()
        for theme_name in themes:
            action = theme_menu.addAction(theme_name.replace('_', ' ').title())
            action.triggered.connect(lambda _, name=theme_name: self.theme_manager.set_theme_action(name))
            
        # Menú de Idiomas
        lang_menu = menu_bar.addMenu(self.i18n.get_text("language_menu"))
        for lang_code in self.i18n.get_available_locales():
            lang_action = lang_menu.addAction(self.i18n.get_text(lang_code))
            lang_action.triggered.connect(lambda _, code=lang_code: self.change_language(code))
        
        # Menú Ayuda
        help_menu = menu_bar.addMenu(self.i18n.get_text("help_menu"))
        about_action = help_menu.addAction(self.i18n.get_text("about_action"))
        about_action.triggered.connect(self.show_about_dialog) # Reemplazar con la función real

    def change_language(self, lang_code):
        self.i18n.set_locale(lang_code)
        self.settings.setValue('locale', lang_code)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(self.i18n.get_text("untitled_document"))
        self.file_manager_widget.setAccessibleName(self.i18n.get_text("file_manager_accessible_name"))
        self.editor.setAccessibleName(self.i18n.get_text("editor_accessible_name"))
        self.preview.setAccessibleName(self.i18n.get_text("preview_accessible_name"))
        self.menuBar().clear()
        self.create_menus()

    def open_selected_file(self, index):
        file_path = self.file_model.filePath(index)
        if os.path.isfile(file_path):
            self.open_file(file_path)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, self.i18n.get_text("open_dialog_title"), "", f"{self.i18n.get_text('markdown_files_filter')} (*.md);;{self.i18n.get_text('all_files_filter')} (*)")
        if file_path:
            self.open_file(file_path)

    def open_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.editor.setPlainText(f.read())
            self.current_file = file_path
            self.setWindowTitle(f"Marque - {os.path.basename(file_path)}")
        except Exception as e:
            QMessageBox.warning(self, self.i18n.get_text("error_open_title"), f"{self.i18n.get_text('error_open_message')}:\n{e}")

    def save_file(self):
        if self.current_file:
            self.save_to_path(self.current_file)
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, self.i18n.get_text("save_as_dialog_title"), "", f"{self.i18n.get_text('markdown_files_filter')} (*.md);;{self.i18n.get_text('all_files_filter')} (*)")
        if file_path:
            if not file_path.endswith('.md'):
                file_path += '.md'
            self.save_to_path(file_path)

    def save_to_path(self, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            self.current_file = file_path
            self.setWindowTitle(f"Marque - {os.path.basename(file_path)}")
        except Exception as e:
            QMessageBox.warning(self, self.i18n.get_text("error_save_title"), f"{self.i18n.get_text('error_save_message')}:\n{e}")

    def update_preview(self):
        markdown_text = self.editor.toPlainText()
        html_output = markdown.markdown(markdown_text)
        self.preview.setHtml(html_output)

    def show_about_dialog(self):
        # Placeholder para la ventana "Acerca de..."
        QMessageBox.information(self, self.i18n.get_text("about_action"), self.i18n.get_text("about_message"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = MarqueEditor()
    editor.show()
    sys.exit(app.exec_())