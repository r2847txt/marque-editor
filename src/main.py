# Lógica de inicio de la aplicación.

import sys
from PyQt5.QtWidgets import QApplication
from ui_editor import MarqueEditor

def main():
    """
    Función principal para iniciar la aplicación Marque.
    """
    # Crea una instancia de QApplication, esencial para cualquier aplicación PyQt5
    app = QApplication(sys.argv)
    
    # Crea una instancia de la ventana principal de nuestro editor
    editor = MarqueEditor()
    
    # Muestra la ventana
    editor.show()
    
    # Inicia el bucle de eventos de la aplicación
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()