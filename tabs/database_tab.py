# -*- coding: utf-8 -*-
import time
from PyQt5 import QtGui, QtCore, uic, QtWidgets
from database.database_table_definitions import Vocabulary_Table, Deleted_Vocabulary_Table, Config_Table, Metadata_Table,  Activity_Table
from dialogs.edit_single_card_dialog import SingleEditDialogClass
from dialogs.edit_multiple_cards_dialog import MultipleEditDialogClass
from dialogs.misc_dialogs import miscDialogs

# Manage and show the items in TableView Widget
class DatabaseTabClass(object):
    def __init__(self, main_window):
        self.main_window = main_window

        # Create connections
        self.main_window.delete_selected_words_button.clicked.connect(lambda: self.delete_cards_slot())
        self.main_window.edit_selected_words.clicked.connect(lambda: self.edit_voc())
        self.main_window.communicate.editing_finished_signal.connect(self.fill_table)

        # Create header variable
        self.header = [self.main_window.tr('Card ID'), self.main_window.tr('Front-side'), self.main_window.tr('Back-side'), self.main_window.tr('Next practice'), self.main_window.tr('Deck'), self.main_window.tr('Course')]

        # standard item model
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(self.header)

        # filter proxy model
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterKeyColumn(-1)
        self.filter_proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        # line edit for filtering
        self.filter_proxy_model.setFilterRegExp(unicode(self.main_window.searchBox.text()))
        self.main_window.searchBox.textChanged.connect(self.filter_proxy_model.setFilterRegExp)

        # Connect tableview widget with filter_proxy_model
        self.main_window.vocabularyList.setModel(self.filter_proxy_model)

        # Set column Width
        self.main_window.vocabularyList.setColumnWidth(0, 70)
        self.main_window.vocabularyList.setColumnWidth(1, 240)
        self.main_window.vocabularyList.setColumnWidth(2, 240)
        self.main_window.vocabularyList.setColumnWidth(3, 160)
        self.main_window.vocabularyList.setColumnWidth(4, 75)

    def fill_table(self):
        self.voclist = self.main_window.session.query(Vocabulary_Table).all()


        # Fill standard item model with data
        item = QtGui.QStandardItem
        for row in range(0, len(self.voclist)):
            word = self.voclist[row]

            self.model.setItem(row, 0, item(str(word.card_id)))
            self.model.setItem(row, 0, item(str(word.card_id)))
            self.model.setItem(row, 1, item(word.front))
            self.model.setItem(row, 2, item(word.back))
            self.model.setItem(row, 3, item(str(word.date_next_practice)))
            self.model.setItem(row, 4, item(str(word.deck)))
            self.model.setItem(row, 5, item(word.course_name))

    def get_selected_cards(self):
        """
        Returns a list with all card_ids of the selected cards in the listview.
        If there are no selected cards an error message will pop up.

        """
        indexes = self.main_window.vocabularyList.selectionModel().selectedRows()
        selected_cards = []
        for self.voc_nr in sorted(indexes):
            selected_cards.append(int(self.voc_nr.data()))

        if len(selected_cards)==0:
            miscDialogs(self.main_window).NoSelectionMessageBox()

        return selected_cards

    def edit_voc(self):
        """

        Get the selected cards and starts a edit dialog class

        """
        cards_to_edit = self.get_selected_cards()

        if len(cards_to_edit)==1:
            self.main_window.edit_single_Dlg = SingleEditDialogClass(cards_to_edit, self.main_window)
            self.main_window.edit_single_Dlg.show()
        elif len(cards_to_edit)>=1:
            self.main_window.edit_multiple_Dlg = MultipleEditDialogClass(cards_to_edit, self.main_window)
            self.main_window.edit_multiple_Dlg.show()


        # Update QTableView by emitting the "editing_finished_signal"
        self.main_window.communicate.editing_finished_signal.emit()

    def delete_cards_slot(self):
        list_of_cards = self.get_selected_cards()
        self.main_window.regular_db_tasks.show_delete_dialog(list_of_cards)