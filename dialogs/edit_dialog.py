# -*- coding: utf-8 -*-
import os
from PyQt5 import uic, QtWidgets

# CLASS WHICH OPENS THE "Edit Dialog"
class EditDialogClass(QtWidgets.QDialog):
    def __init__(self, words_to_edit_list, main_window, communicate):
        QtWidgets.QDialog.__init__(self)
        uic.loadUi(os.path.abspath(u'./ui_resources/edit_word.ui'), self)
        self.words_to_edit_list = words_to_edit_list
        self.main_window = main_window
        self.communicate = communicate

        if appSettings.value("mainConfig/languageFeatureKey", False) == False:
            self.language_combo.hide()

        elif appSettings.value("mainConfig/languageFeatureKey", False) == True:
            self.language_combo.clear()
            if appSettings.value("languageFeature/Language0Key", "Default") != '':
                self.language_combo.addItem(appSettings.value("languageFeature/Language0Key", "Default"))
            if appSettings.value("languageFeature/Language1Key", "") != '':
                self.language_combo.addItem(appSettings.value("languageFeature/Language1Key", ""))
            if appSettings.value("languageFeature/Language2Key", "") != '':
                self.language_combo.addItem(appSettings.value("languageFeature/Language2Key", ""))
            if appSettings.value("languageFeature/Language3Key", "") != '':
                self.language_combo.addItem(appSettings.value("languageFeature/Language3Key", ""))



        self.delete_item.clicked.connect(self.delete_voc)
        self.ed_ok.clicked.connect(self.save_changes)

        self.load_new_word()

    # LOADS A NEW WORD INTO THE DIALOG IF THERE ARE STILL ITEMS IN THE "words_to_edit_list". IF THERE ARE NO ITEMS LEFT IN THE LIST, THE DIALOG WILL BE CLOSED
    def load_new_word(self):
        if not len(self.words_to_edit_list) ==0:
            self.current_word = self.words_to_edit_list[0]

            self.language_combo.setCurrentIndex(self.language_combo.findText(self.current_word.language))

            self.select_step.setValue(int(self.current_word.deck))
            self.select_step.setSuffix('')
            self.select_step.setPrefix('')

            self.vorderseite_edit.setPlainText(self.current_word.front)
            self.rueckseite_edit.setPlainText(self.current_word.back)

            del self.words_to_edit_list[0]

        else:
            self.close()

    # DELETE THE CURRENT WORD
    def delete_voc(self):
        self.appSettings.delete_data(self.current_word.id)

        # Update QTableView by emitting the "editing_finished_signal"
        self.communicate.editing_finished_signal.emit()
        self.load_new_word()


    # SAVE THE CHANGES
    def save_changes(self):
        new_language = self.language_combo.currentIndex()
        if new_language == -1:
            new_language = 0

        new_frontside = unicode(self.vorderseite_edit.toPlainText())
        new_backside = unicode(self.rueckseite_edit.toPlainText())
        new_phase = self.select_step.value()

        self.appSettings.edit_voc(new_phase, new_frontside, new_backside, self.current_word.id, new_language)

        # Update QTableView by emitting the "editing_finished_signal"
        self.communicate.editing_finished_signal.emit()

        self.load_new_word()