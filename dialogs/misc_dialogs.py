from PyQt5 import uic, QtWidgets
import os

# ABOUT DIALOG
class miscDialogs(QtWidgets.QDialog):
    def __init__(self, main_window):
        self.main_window = main_window

    def NoSelectionMessageBox(self):
        error = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, self.main_window.tr("No card selected"),
                                      self.main_window.tr("No card selected. Select a card first!"))
        error.exec_()

    def RequiredInformationMessageBox(self):
        error = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, self.main_window.tr("Missing Information"),
                                      self.main_window.tr(
                                          "Not all required information have been provided. Please check your entry!"))
        error.exec_()