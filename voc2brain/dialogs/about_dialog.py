from PyQt5 import uic, QtWidgets
import os

# ABOUT DIALOG
class aboutDialog(QtWidgets.QDialog):
    # Class for the dialog about the program
    def __init__(self):
        print '###################################'
        QtWidgets.QDialog.__init__(self)
        uic.loadUi(os.path.abspath(u'./ui_resources/about.ui'), self)