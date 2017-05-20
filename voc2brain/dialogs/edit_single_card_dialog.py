# -*- coding: utf-8 -*-
import os
from PyQt5 import uic, QtWidgets
from database.database_table_definitions import Vocabulary_Table, Deleted_Vocabulary_Table, Config_Table, Metadata_Table, Activity_Table

# CLASS WHICH HANDLES THE "Edit Dialog"
class SingleEditDialogClass(QtWidgets.QDialog):
    def __init__(self, cards_to_edit, main_window):
        QtWidgets.QDialog.__init__(self)
        uic.loadUi(os.path.abspath(u'./ui_resources/edit_single_card.ui'), self)

        self.card_id_current_card = cards_to_edit[0]
        self.main_window = main_window

        self.delete_item.clicked.connect(self.delete_voc)
        self.ed_ok.clicked.connect(self.save_changes)

        self.load_new_card()

    def load_new_card(self):
        """
        Loads a new card into the dialog.

        """
        print int(self.card_id_current_card)
        self.current_word = self.main_window.session.query(Vocabulary_Table).filter_by(card_id=int(self.card_id_current_card)).first()

        self.course_combo.setCurrentIndex(self.course_combo.findText(self.current_word.course_name))

        # Uncomment when lesson feature gets rolled out
        #self.lesson_combo.setCurrentIndex(self.lesson_combo.findText(self.current_word.lesson_name))
        self.lesson_frame.hide()

        self.deck_spinbox.setValue(int(self.current_word.deck))
        self.deck_spinbox.setSuffix('')
        self.deck_spinbox.setPrefix('')

        self.front_side_textedit.setPlainText(self.current_word.front)
        self.flip_side_textedit.setPlainText(self.current_word.back)

    def delete_voc(self):
        """
        Deletes the card

        """
        card = self.current_word
        self.main_window.session.delete(card)

        # Update QTableView by emitting the "editing_finished_signal"
        self.main_window.communicate.editing_finished_signal.emit()

        self.close()

    def save_changes(self):
        """
        Save the changes

        """
        new_card = self.course_combo.currentIndex()
        if new_card == -1:
            new_card = 0

        new_frontside = unicode(self.front_side_textedit.toPlainText())
        new_backside = unicode(self.flip_side_textedit.toPlainText())
        new_deck = self.deck_spinbox.value()
        new_course = self.course_combo.currentText()
        update_dict = {'deck': new_deck, "course_name":new_course, "front":new_frontside, "back": new_backside}

        # Add lesson if the organise lessons feature is activated
        if self.main_window.config.get("mainConfig/organise_lessons_feature") == 0:
            new_lesson = self.lesson_combo.currentText()
            update_dict["lesson_name"] = new_lesson

        # Send Changes to Database
        self.main_window.session.query(Vocabulary_Table).filter_by(card_id=card_id_current_card).update(update_dict)
        self.main_window.session.commit()

        # Update QTableView by emitting the "editing_finished_signal"
        self.main_window.communicate.editing_finished_signal.emit()

        self.close()