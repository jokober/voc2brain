# -*- coding: utf-8 -*-
import time
from PyQt5 import QtGui, QtCore, uic, QtWidgets
from database.database_table_definitions import Vocabulary_Table, Deleted_Vocabulary_Table, Config_Table, Metadata_Table,  Activity_Table
from dialogs.edit_single_card_dialog import SingleEditDialogClass
from dialogs.misc_dialogs import miscDialogs

# Manage and show the items in TableView Widget
class DatabaseTabClass(object):
    def __init__(self, main_window):
        self.main_window = main_window

        # Create connections
        self.main_window.delete_selected_words_button.clicked.connect(lambda: self.delete_vocs())
        self.main_window.edit_selected_words.clicked.connect(lambda: self.edit_voc())
        self.main_window.communicate.editing_finished_signal.connect(self.fill_table)

        # Create header variable
        self.header = [self.main_window.tr('Front-side'), self.main_window.tr('Back-side'), self.main_window.tr('Next practice'), self.main_window.tr('Deck'), self.main_window.tr('Course')]

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
        self.main_window.vocabularyList.setColumnWidth(0, 240)
        self.main_window.vocabularyList.setColumnWidth(1, 240)
        self.main_window.vocabularyList.setColumnWidth(2, 160)
        self.main_window.vocabularyList.setColumnWidth(3, 75)

    def fill_table(self):
        self.voclist = self.main_window.session.query(Vocabulary_Table).all()
        print type(self.voclist)
        print self.voclist

        # Fill standard item model with data
        item = QtGui.QStandardItem
        for row in range(0, len(self.voclist)):
            word = self.voclist[row]
            self.model.setItem(row, 0, item(word.front))
            self.model.setItem(row, 1, item(word.back))
            self.model.setItem(row, 2, item(str(word.date_next_practice)))
            self.model.setItem(row, 3, item(str(word.deck)))
            self.model.setItem(row, 4, item(word.course_name))


    # GET SELECTED WORDS AND STARTS DIE "EDIT" DIALOG CLASS
    def edit_voc(self):
        print "edit..."
        indexes = self.main_window.vocabularyList.selectionModel().selectedRows()
        cards_to_edit = []
        for self.voc_nr in sorted(indexes):
            cards_to_edit.append(self.voc_nr)

        if len(cards_to_edit)==1:
            self.main_window.edDlg = SingleEditDialogClass(cards_to_edit[0], self.main_window)
            self.main_window.edDlg.show()
        elif len(cards_to_edit)>=1:
            pass
        elif len(cards_to_edit)==0:
            miscDialogs(self.main_window).NoSelectionMessageBox()

        # Update QTableView by emitting the "editing_finished_signal"
        self.main_window.communicate.editing_finished_signal.emit()

    # GET SELECTED WORDS AND DELETE THEM
    def delete_vocs(self):
        ask_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, self.main_window.tr("Delete words"),
            self.main_window.tr("Do you really want to delete the selected cards?"))
        ask_message.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        ret = ask_message.exec_()

        if ret == QtWidgets.QMessageBox.Yes:
            indexes = self.main_window.vocabularyList.selectionModel().selectedRows()

            # Delete all selected cards from "Vocabulary_Table" and add them to the "Deleted_Vocabulary_Table
            for self.voc_nr in sorted(indexes):
                card = self.main_window.session.query(Vocabulary_Table).filter(Vocabulary_Table.id ==self.voc_nr.data()).first()
                print unicode(card)
                self.main_window.session.delete(card)

                self.main_window.session.add(Deleted_Vocabulary_Table(delete_date = time.time(), front = card.front, back = card.back ))
                self.main_window.session.commit()

                # Update QTableView by emitting the "editing_finished_signal"
                self.main_window.communicate.editing_finished_signal.emit()

        else:
            pass

class Database_TreeWidgetClass(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.addItems(self.main_window.course_treeWidget.invisibleRootItem())
        self.main_window.course_treeWidget.itemChanged.connect (self.handleChanged)

    def addItems(self, parent):
        column = 0
        for course_string in self.main_window.session.query(Vocabulary_Table.course_name).distinct():
            course_item = self.addParent(parent, column, unicode(course_string.course_name), 'data Clients')

            for lesson_string in self.main_window.session.query(Vocabulary_Table.lesson_name).filter_by(course_name=course_string.course_name).distinct():
                self.addChild(course_item, column, lesson_string.lesson_name, 'data Type A')

        """
        vendors_item = self.addParent(parent, column, 'Vendors', 'data Vendors')
        time_period_item = self.addParent(parent, column, 'Time Period', 'data Time Period')

        self.addChild(clients_item, column, 'Type A', 'data Type A')
        self.addChild(clients_item, column, 'Type B', 'data Type B')
        """

    def addParent(self, parent, column, title, data):
        item = QtWidgets.QTreeWidgetItem(parent, [title])
        item.setData(column, QtCore.Qt.UserRole, data)
        item.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.ShowIndicator)
        item.setExpanded (True)
        return item

    def addChild(self, parent, column, title, data):
        item = QtWidgets.QTreeWidgetItem(parent, [title])
        item.setData(column, QtCore.Qt.UserRole, data)
        item.setCheckState (column, QtCore.Qt.Unchecked)
        return item

    def handleChanged(self, item, column):
        if item.checkState(column) == QtCore.Qt.Checked:
            print "checked", item, item.text(column)
        if item.checkState(column) == QtCore.Qt.Unchecked:
            print "unchecked", item, item.text(column)