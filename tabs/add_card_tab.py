# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
import time
import datetime
from database.database_table_definitions import Vocabulary_Table, Deleted_Vocabulary_Table, Config_Table, Metadata_Table,  Activity_Table


# ADD NEW WORD TO THE DATABASE
class AddCardTab_class(object):
    def __init__(self, main_window):
        self.main_window = main_window

        self.main_window.add_card_button.clicked.connect(lambda: self.add_card())

        # fill combobox with course_names
        self.main_window.course_comboBox.clear()
        for result in self.main_window.session.query(Vocabulary_Table.course_name).distinct().all():
            self.main_window.course_comboBox.addItem(result.course_name)

    def add_card(self):
        frontside = unicode(self.main_window.front_input_textedit.toPlainText())
        backside = unicode(self.main_window.back_input_textedit.toPlainText())

        if frontside and backside:
            first_interrogation = datetime.date.today()
            card_course = self.main_window.course_comboBox.currentText()
            lesson_name = ""
            createdDate= datetime.date.today()

            self.main_window.session.add(
                Vocabulary_Table(front=frontside, back=backside, date_next_practice=first_interrogation, deck=0,
                                 course_name=card_course, lesson_name = lesson_name, createdDate=createdDate))

            # Adds two words if "Reverse Translation" is checked
            if self.main_window.create_reverse_card_checkbox.checkState() == 2:
                self.main_window.session.add(Vocabulary_Table(front=backside, back=frontside, date_next_practice=first_interrogation, deck=0, course_name=card_course, lesson_name = lesson_name, createdDate=createdDate))

            # Empty the QTextEdit areas
            self.main_window.front_input_textedit.setPlainText(u'')
            self.main_window.back_input_textedit.setPlainText(u'')

            # Commit to db
            self.main_window.session.commit()

        else:
            error = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, self.main_window.tr("Failing entry"),
                                          self.main_window.tr("Please check your entry!"))
            error.exec_()