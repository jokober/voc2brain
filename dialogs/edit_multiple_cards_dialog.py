# -*- coding: utf-8 -*-
import os
from PyQt5 import uic, QtWidgets, QtGui
from edit_single_card_dialog import SingleEditDialogClass
from database.database_table_definitions import Vocabulary_Table, Deleted_Vocabulary_Table, Config_Table, Metadata_Table, Activity_Table, Course_Table

# CLASS WHICH HANDLES THE "Edit Dialog"
class MultipleEditDialogClass(QtWidgets.QDialog):
    def __init__(self, cards_to_edit, main_window):
        QtWidgets.QDialog.__init__(self)
        uic.loadUi(os.path.abspath(u'./ui_resources/edit_multiple_cards.ui'), self)
        self.main_window = main_window

        self.cards_to_edit = cards_to_edit
        self.cards_to_edit_query = self.main_window.session.query(Vocabulary_Table).filter(
                Vocabulary_Table.card_id.in_(self.cards_to_edit))

        self.delete_cards.clicked.connect(lambda: self.delete_cards_slot())
        self.edit_voc_button.clicked.connect(self.edit_voc)
        self.ed_ok.clicked.connect(self.save_changes_multiple_cards)

        self.fill_edit_treeview()

        for card in self.main_window.session.query(Course_Table.course_name).distinct().all():
            self.course_combo.addItem(card.course_name)


    def fill_edit_treeview(self):
        """
        Fills the treeview with items

        """
        self.edit_voc_treeview_model = QtGui.QStandardItemModel()
        header = [self.main_window.tr('Card ID'),
                  self.main_window.tr('Front-side'),
                  self.main_window.tr('Back-side'),
                  self.main_window.tr('Deck'),
                  self.main_window.tr('Course')
                  ]

        # Add lesson header if the organise lessons feature is activated
        if self.main_window.config.get("mainConfig/organise_lessons_feature") == 0:
            header.append(self.main_window.tr('Lesson'))

        self.edit_voc_treeview_model.setHorizontalHeaderLabels(header)

        parentItem = self.edit_voc_treeview_model

        for current_word in self.cards_to_edit_query:
            row_list = [QtGui.QStandardItem(str(current_word.card_id)),
                        QtGui.QStandardItem(current_word.front),
                        QtGui.QStandardItem(current_word.back),
                        QtGui.QStandardItem(str(current_word.deck)),
                        QtGui.QStandardItem(current_word.course_name)
                        ]

            # Add lesson header if the organise lessons feature is activated
            if self.main_window.config.get("mainConfig/organise_lessons_feature") == 0:
                row_list.append(QtGui.QStandardItem(current_word.lesson_name))

            parentItem.appendRow(row_list)


        self.cards_to_edit_treeView.setModel(self.edit_voc_treeview_model)

    def delete_cards_slot(self):
        """
        Deletes all cards

        """
        list_of_cards = self.cards_to_edit
        self.main_window.regular_db_tasks.show_delete_dialog(list_of_cards)

    def edit_voc(self):
        index = self.cards_to_edit_treeView.selectionModel().selectedRows()
        cards_to_edit = [index[0].data()]

        self.main_window.edit_single_Dlg = SingleEditDialogClass(cards_to_edit, self.main_window)
        self.main_window.edit_single_Dlg.show()

    # SAVE THE CHANGES
    def save_changes_multiple_cards(self):
        new_deck = self.deck_spinbox.value()
        new_course = self.course_combo.currentText()
        update_dict = {'deck': new_deck, "course_name":new_course}

        # Add lesson if the organise lessons feature is activated
        #if self.main_window.config.get("mainConfig/organise_lessons_feature") == 0:
        #    new_lesson = self.lesson_combo.currentText()
        #    update_dict["lesson_name"] = new_lesson

        # Send Changes to Database
        self.main_window.session.query(Vocabulary_Table).filter_by(card_id=card_id).update(update_dict)
        self.main_window.session.commit()

        # Update QTableView by emitting the "editing_finished_signal"
        self.main_window.communicate.editing_finished_signal.emit()

