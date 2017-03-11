# -*- coding: utf-8 -*-
import os
from PyQt5 import uic, QtWidgets

# CLASS WHICH HANDLES THE "Edit Dialog"
class SingleEditDialogClass(QtWidgets.QDialog):
    def __init__(self, words_to_edit_list, main_window, communicate):
        QtWidgets.QDialog.__init__(self)
        uic.loadUi(os.path.abspath(u'./ui_resources/edit_single_card.ui'), self)

        self.words_to_edit_list = words_to_edit_list
        self.main_window = main_window
        self.communicate = communicate

        self.delete_item.clicked.connect(self.delete_voc)
        self.ed_ok.clicked.connect(self.save_changes)

        self.load_new_card()

    # LOADS A NEW WORD INTO THE DIALOG IF THERE ARE STILL ITEMS IN THE "words_to_edit_list". IF THERE ARE NO ITEMS LEFT IN THE LIST, THE DIALOG WILL BE CLOSED
    def load_new_card(self):
        if not len(self.words_to_edit_list) ==0:
            self.current_word = self.words_to_edit_list[0]

            self.course_combo.setCurrentIndex(self.course_combo.findText(self.current_word.course))

            self.lesson_combo.setCurrentIndex(self.lesson_combo.findText(self.current_word.lesson))

            self.select_step.setValue(int(self.current_word.deck))
            self.select_step.setSuffix('')
            self.select_step.setPrefix('')

            self.front_side_textedit.setPlainText(self.current_word.front)
            self.flip_side_textedit.setPlainText(self.current_word.back)

            del self.words_to_edit_list[0]

        else:
            self.close()

    # DELETE THE CURRENT WORD
    def delete_voc(self):
        card = self.current_word.card_id
        self.main_window.session.delete(card)

        # Update QTableView by emitting the "editing_finished_signal"
        self.communicate.editing_finished_signal.emit()
        self.load_new_card()


    # SAVE THE CHANGES
    def save_changes(self):
        new_card = self.course_combo.currentIndex()
        if new_card == -1:
            new_card = 0

        new_frontside = unicode(self.front_side_textedit.toPlainText())
        new_backside = unicode(self.flip_side_textedit.toPlainText())
        new_deck = self.deck_spinbox.value()
        new_course = self.course_combo.currentText()
        new_lesson = self.lesson_combo.currentText()

        self.main_window.session.query(Vocabulary_Table).filter_by(card_id=card_id).update(
            {'deck': new_deck, "front": new_frontside, "back":new_backside, "course":new_course, "new_lesson": new_lesson})

        # Update QTableView by emitting the "editing_finished_signal"
        self.communicate.editing_finished_signal.emit()

        self.load_new_card()