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
        self.main_window.edit_course_name_button.clicked.connect(lambda: self._rename_course())
        self.main_window.course_manager_treeView.selectionModel().selectionChanged.connect(lambda: self._load_course())

    # FILLS THE TREEVIEW WIDGET WITH COURSE NAMES
    def fill_course_treeview(self):
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
    # LOAD UI ELEMENTS BASED ON CURRENTLY SELECTED COURSE
    def _load_course(self):

        # get currently selected course
        index = self.main_window.course_manager_treeView.selectionModel().selectedRows()
        if len(index) ==1:
            current_course_name = unicode(index[0].data())

        self.main_window.course_name_lineedit.setText(current_course_name)

    # GET THE CURRENTLY SELECTED COURSE AND RETURNS IT AS UNICODE
    def _get_selected_course(self):
        index = self.main_window.course_manager_treeView.selectionModel().selectedRows()
        if len(index) == 1:
            current_course_name =  unicode(index[0].data())
        else:
            return 'no course selected'
        return current_course_name

    # LOAD UI ELEMENTS BASED ON CURRENTLY SELECTED COURSE
    def _load_course(self):
        current_course_name = unicode(self._get_selected_course())
        self.main_window.course_name_label.setText(unicode(current_course_name))

    def _rename_course(self):
        current_course_name = self._get_selected_course()

        new_course_name, ok = QtWidgets.QInputDialog.getText(self.main_window, self.main_window.tr('Edit Course Name'), self.main_window.tr('Enter a new name for this course:'), QtWidgets.QLineEdit.Normal, current_course_name)

        if ok:
            # updade course names in all cards
            self.main_window.session.query(Course_Table.course_name).filter_by(course_name=current_course_name).update({'course_name': new_course_name})
            self.main_window.session.commit()

            # load ui elements
            self.fill_course_treeview()

    def create_course(self):
        new_course, ok = QtWidgets.QInputDialog.getText(self.main_window, self.main_window.tr('Create Course'), self.main_window.tr('Enter a name for the new course:'))

        if ok:
            # updade course names in all cards
            self.main_window.session.add(Course_Table(course_name = new_course))
            self.main_window.session.commit()

            # load ui elements
            self.fill_course_treeview()