# -*- coding: utf-8 -*-
import time
from PyQt5 import QtGui, QtCore, uic, QtWidgets
from database.database_table_definitions import Vocabulary_Table, Course_Table, Lesson_Table,Deleted_Vocabulary_Table, Config_Table, Metadata_Table,  Activity_Table
from sqlalchemy import Table

# Manage and show the items in TableView Widget
class CourseTabClass(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.fill_course_treeview()
        self.fill_lessons_treeview()

        self.main_window.add_course_button.clicked.connect(lambda: self.create_course())
        self.main_window.edit_course_name_button.clicked.connect(lambda: self.rename_course())
        self.main_window.course_manager_treeView.selectionModel().selectionChanged.connect(lambda: self._load_course())


    def fill_course_treeview(self):
        """
        Fills the treeview with items

        """
        self.course_treeview_model = QtGui.QStandardItemModel()
        self.course_header = [self.main_window.tr('Courses')]
        self.course_treeview_model.setHorizontalHeaderLabels(self.course_header)

        parentItem = self.course_treeview_model

        for course_string in self.main_window.session.query(Course_Table.course_name).distinct():
            parentItem.appendRow(QtGui.QStandardItem(course_string.course_name))

        self.main_window.course_manager_treeView.setModel(self.course_treeview_model)

        # reload ui elements
        self._load_course()

    # FILLS THE TREEVIEW WIDGET WITH LESSON NAMES
    def fill_lessons_treeview(self):
        pass

        """
        self.lessons_treeview_model = QtGui.QStandardItemModel()

        parentItem = self.lessons_treeview_model.invisibleRootItem()

        for lesson_string in self.main_window.session.query(Vocabulary_Table.lesson_name).distinct():
            item = QtGui.QStandardItem(lesson_string.lesson_name)
            parentItem.appendRow(item)

        self.main_window.lessons_treeView.setModel(self.lessons_treeview_model)
        self.main_window.lessons_manager_treeView.setModel(self.lessons_treeview_model)
        """
    def fill_table_course_cards(self):
        """
        Fills the 'course_cards_tableView' with cards

        """

        # Create header variable
        header = [self.main_window.tr('Front-side'), self.main_window.tr('Back-side'), self.main_window.tr('Next practice'), self.main_window.tr('Deck'), self.main_window.tr('Course')]

        # standard item model
        self.course_cards_model = QtGui.QStandardItemModel()
        self.course_cards_model.setHorizontalHeaderLabels(header)

        # Connect tableview widget with filter_proxy_model
        self.main_window.course_cards_tableView.setModel(self.course_cards_model)

        # Set column Width
        self.main_window.course_cards_tableView.setColumnWidth(0, 240)
        self.main_window.course_cards_tableView.setColumnWidth(1, 240)
        self.main_window.course_cards_tableView.setColumnWidth(2, 160)
        self.main_window.course_cards_tableView.setColumnWidth(3, 75)

        self.course_voclist = self.main_window.session.query(Vocabulary_Table)
        self.course_voclist= self.course_voclist.filter_by(course_name=unicode(self._get_selected_course())).all()

        # Fill standard item model with data
        item = QtGui.QStandardItem
        for row in range(0, len(self.course_voclist)):
            word = self.course_voclist[row]
            self.course_cards_model.setItem(row, 0, item(word.front))
            self.course_cards_model.setItem(row, 1, item(word.back))
            self.course_cards_model.setItem(row, 2, item(str(word.date_next_practice)))
            self.course_cards_model.setItem(row, 3, item(str(word.deck)))
            self.course_cards_model.setItem(row, 4, item(word.course_name))

    def _load_course(self):
        """
        This fuction will run as soon as a new course has been selected in the  'course_manager_treeView'
        It will load the course specific ui-elements and update the 'course_cards_tableView'

        """
        current_course_name = unicode(self._get_selected_course())

        # Update the course label
        self.main_window.course_name_label.setText(current_course_name)

        # Load the cards of the course into the qlistview
        self.fill_table_course_cards()

    # GET THE CURRENTLY SELECTED COURSE AND RETURNS IT AS UNICODE
    def _get_selected_course(self):
        index = self.main_window.course_manager_treeView.selectionModel().selectedRows()
        if len(index) == 1:
            current_course_name =  unicode(index[0].data())
        else:
            return 'no course selected'
        return current_course_name


    def rename_course(self):
        current_course_name = self._get_selected_course()

        new_course_name, ok = QtWidgets.QInputDialog.getText(self.main_window, self.main_window.tr('Edit Course Name'), self.main_window.tr('Enter a new name for this course:'), QtWidgets.QLineEdit.Normal, current_course_name)

        if ok:
            # check if course already exists
            if self.main_window.session.query(Course_Table).filter_by(course_name=new_course_name).first():
                self.show_course_exists_error()
                return

            # updade course names in all cards
            query = self.main_window.session.query(Course_Table.course_name).filter_by(course_name=current_course_name).update({'course_name': new_course_name})
            self.main_window.session.query(Vocabulary_Table.course_name).filter_by(course_name=current_course_name).update({'course_name': new_course_name})
            self.main_window.session.commit()

            # load ui elements
            self.fill_course_treeview()

    def create_course(self):
        new_course, ok = QtWidgets.QInputDialog.getText(self.main_window, self.main_window.tr('Create Course'), self.main_window.tr('Enter a name for the new course:'))
        print "loos"

        if ok:
            # check if course already exists
            if self.main_window.session.query(Course_Table).filter_by(course_name=new_course).first():
                self.show_course_exists_error()
                return

            # updade course names in all cards
            self.main_window.session.merge(Course_Table(course_name = new_course))
            self.main_window.session.commit()

            # load ui elements
            self.fill_course_treeview()

    def show_course_exists_error(self):
        error = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, self.main_window.tr("Course already exists"),
                                           self.main_window.tr(
                                               "A course with the same name already exists. Please choose another name for the course."))
        error.exec_()