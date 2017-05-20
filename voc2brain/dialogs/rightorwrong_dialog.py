# -*- coding: utf-8 -*-

import os, sys
from database.database_table_definitions import Vocabulary_Table, Deleted_Vocabulary_Table, Config_Table, Metadata_Table, Activity_Table
from PyQt5 import QtCore, QtGui, uic, QtWidgets

#Get path for database 
#check os
operating_system = unicode(sys.platform)

class Right_or_Wrong_Class(QtWidgets.QDialog):
    def __init__(self, given_answer, card_id, main_window, mode):
        QtWidgets.QDialog.__init__(self)
        uic.loadUi(os.path.abspath(u'.'+ u'/ui_resources/right_or_wrong.ui'), self)
        self.setWindowTitle(unicode(self.tr('Check your answer')))
        self.main_window = main_window

        self.wrong.activateWindow()
        self.mode=mode
        self.card_id = card_id

        correct_answer = self.main_window.session.query(Vocabulary_Table).filter(Vocabulary_Table.card_id == card_id).first().back

        size =  self.geometry()
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

        if operating_system == 'linux2':
            self.right.setIcon(QtGui.QIcon(os.path.join(os.path.abspath(u'.'), U'icons/right.svg')))
            self.wrong.setIcon(QtGui.QIcon(os.path.join(os.path.abspath(u'.'), U'icons/wrong.svg')))
            
        elif operating_system == 'win32':
            self.right.setIcon(QtGui.QIcon(os.path.join(os.path.abspath(u'.'), u'icons/right.png')))
            self.wrong.setIcon(QtGui.QIcon(os.path.join(os.path.abspath(u'.'), U'icons/wrong.png')))

        self.right.clicked.connect(self.emit_isright)
        self.wrong.clicked.connect(self.emit_iswrong)

        self.correct_answer_textEdit.setPlainText(unicode(correct_answer))
        self.given_answer_textEdit.setPlainText(unicode(given_answer))

    def emit_isright(self):
        if self.mode =="NormalMode":
            self.main_window.communicate.right_answer_signal.emit(self.card_id)
            self.close()
        elif self.mode =="SpeedReview":
            self.close()

    def emit_iswrong(self):
        if self.mode =="NormalMode":
            self.main_window.communicate.wrong_answer_signal.emit(self.card_id)
            self.close()
        elif self.mode =="SpeedReview":
            self.close()

