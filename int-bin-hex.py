import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from pyqt_gui import Ui_MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # set application style based on platform
    if sys.platform == "win32":
        app.setStyle("Fusion")  # Use Fusion style on Windows
    elif sys.platform == "darwin":
        app.setStyle("Macintosh")  # Use Macintosh style on macOS
    else:
        app.setStyle("Breeze")  # Use Breeze style on Linux

    # create color palette and set to app
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
    app.setPalette(dark_palette)
    # set style for tooltip
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)

    # set font for components
    ui.binOutput.setFont(QtGui.QFont("Consolas", 8))
    ui.hexOutput.setFont(QtGui.QFont("Consolas", 8))
    ui.intOutput.setFont(QtGui.QFont("Consolas", 8))
    ui.inputField.setFont(QtGui.QFont("Consolas", 8))
    ui.comboBox.setFont(QtGui.QFont("Consolas", 8))

    # Add options to the combo box
    ui.comboBox.addItems(["Integer", "Binary", "Hexadecimal"])

    # Method for converting input and outputting in int, bin, and hex
    def convert():
        input_text = ui.inputField.text().strip()
        combo_box_text = ui.comboBox.currentText()

        def invalid_input(message):
            QMessageBox.critical(mainWindow, "Error", message)

        if input_text:
            parts = input_text.split(".")
            output_int, output_bin, output_hex = [], [], []

            for part in parts:
                try:
                    if combo_box_text == "Integer":
                        input_value = int(part)
                        output_int.append(str(input_value))
                        output_bin.append(bin(input_value)[2:])
                        output_hex.append(hex(input_value)[2:].upper())
                    elif combo_box_text == "Binary":
                        if all(bit in "01" for bit in part):
                            input_value = int(part, 2)
                            output_int.append(str(input_value))
                            output_bin.append(part)
                            output_hex.append(hex(input_value)[2:].upper())
                        else:
                            invalid_input("Invalid {} Input!".format(combo_box_text))
                            return
                    elif combo_box_text == "Hexadecimal":
                        if all(char in "0123456789ABCDEFabcdef" for char in part):
                            input_value = int(part, 16)
                            output_int.append(str(input_value))
                            output_bin.append(bin(input_value)[2:])
                            output_hex.append(part.upper())
                        else:
                            invalid_input("Invalid {} Input!".format(combo_box_text))
                            return
                except ValueError:
                    invalid_input("Invalid {} Input!".format(combo_box_text))
                    return

            ui.intOutput.appendPlainText(".".join(output_int))
            ui.binOutput.appendPlainText(".".join(output_bin))
            ui.hexOutput.appendPlainText(".".join(output_hex))
            
    # Connect the "clicked" signal of the convertButton to the convert_text function
    ui.convertButton.clicked.connect(convert)
    # Connect the "returnPressed" signal of the inputField to the convert function
    ui.inputField.returnPressed.connect(convert)

    # Method for syncronizing the scrollbars of the output fields
    def sync_scrollbars(source_scrollbar_value):
        ui.intOutput.verticalScrollBar().setValue(source_scrollbar_value)
        ui.binOutput.verticalScrollBar().setValue(source_scrollbar_value)
        ui.hexOutput.verticalScrollBar().setValue(source_scrollbar_value)
    # Connect the valueChanged signal of the source QPlainTextEdit to the sync_scrollbars function
    ui.intOutput.verticalScrollBar().valueChanged.connect(sync_scrollbars)
    ui.binOutput.verticalScrollBar().valueChanged.connect(sync_scrollbars)
    ui.hexOutput.verticalScrollBar().valueChanged.connect(sync_scrollbars)

    # Set window flags to prevent maximizing and resizing
    mainWindow.setWindowFlags(mainWindow.windowFlags() & ~Qt.WindowMaximizeButtonHint)
    mainWindow.setFixedSize(mainWindow.size())

    mainWindow.show()
    sys.exit(app.exec_())