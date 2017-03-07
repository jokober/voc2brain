from PyQt5 import uic, QtWidgets
import os

# ABOUT DIALOG
class aboutDialog(QtWidgets.QDialog):
    # Class for the dialog about the program
    def __init__(self):
        print '###################################'
        QtWidgets.QDialog.__init__(self)
        uic.loadUi(os.path.abspath(u'./ui_resources/about.ui'), self)

        self.translator_link.clicked.connect(self.open_translator_web)

    def open_translator_web(self):
        webbrowser.open_new_tab("http://voc2brain.sourceforge.net/?page_id=95")