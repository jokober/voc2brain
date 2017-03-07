# -*- coding: utf-8 -*-

import os
from PyQt5 import QtCore, uic, QtWidgets

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Voc2brain_latest.misc.custom_signals import Communicate
from Voc2brain_latest.tabs.init_main_window import init_main_window_class
from database.database_migrate import DatabaseMigrateClass
from dialogs.language_switcher import lsDialog
from misc.os_adjustments import os_adjustment_object

from tabs.configuration_tab import ConfigurationTabClass
from tabs.database_tab import DatabaseTabClass
from tabs.practice_tab import PracticeTabClass
from tabs.stats_tab import StatsTabClass
from tabs.course_tab import CourseTabClass
from tabs.add_card_tab import AddCardTab_class

# MAIN LOOP
durchl = 0
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, voc2brain_app):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi(os.path.abspath(u'.' + u'/ui_resources/MainWindow.ui'), self)

        # Get all custom signals
        self.communicate = Communicate()

        self.voc2brain_app = voc2brain_app


        # Create sqlalchemy engine and session
        self.local_engine = create_engine('sqlite:///'+ os_adjustment_object.database_path, isolation_level="READ UNCOMMITTED", echo= True )

        self.Session = sessionmaker(bind=self.local_engine)
        self.session = self.Session()

        from database.database_table_definitions import *
        self.base = Base
        self.base.metadata.create_all(self.local_engine, checkfirst=True)

        # Migrate database to newer version if applicable
        DatabaseMigrateClass(self).check_version()

        # Prepare the ui
        init_main_window_class(self)

        self.MainTabs.currentChanged.connect(self.whichTab)

        # Prepare configurations
        ConfigurationTabClass(self)

    def __run__(self):
        pass

    # THIS WILL START THE INDIVIDUAL "tab_classes"
    def whichTab(self):
        if self.MainTabs.currentIndex() == self.MainTabs.indexOf(self.stats_tab_page):
            StatsTabClass(self)
        if self.MainTabs.currentIndex() == self.MainTabs.indexOf(self.practice_tab_page):
            self.flip_side_textedit.setFocus()
            PracticeTabClass(self)
        if self.MainTabs.currentIndex() == self.MainTabs.indexOf(self.database_tab_page):
            DatabaseTabClass(self).fill_table()
        if self.MainTabs.currentIndex() == self.MainTabs.indexOf(self.configuration_tab_page):
            ConfigurationTabClass(self)
        if self.MainTabs.currentIndex() == self.MainTabs.indexOf(self.course_tab_page):
            CourseTabClass(self)
        if self.MainTabs.currentIndex() == self.MainTabs.indexOf(self.add_card_tab_page):
            AddCardTab_class(self)



    def translate_ui(self):
        self.translator = QtCore.QTranslator()

        if self.session.query(config_table).filter(config_table.key == "localization/LanguageKey") != 'no_file':
            print "### Info ### Use translation file]"
            self.translator.load(lsDialog(self).get_tr_file() + '.qm', './translation/')
        else:
            print "### Info ### Use system language"
            if QtCore.QLocale.system().name().split('_')[0] != 'en':
                self.translator.load(u'voc2brain_' + QtCore.QLocale.system().name().split('_')[0] + '.qm', './translation/')
        app.installTranslator(self.translator)

    def closeEvent(self,event):
        # uncomment if you want Voc2brain should ask before closing
        """result = QtWidgets.QMessageBox.question(self,
                      "Confirm Exit...",
                      "Are you sure you want to exit ?",
                      QtWidgets.QMessageBox.Yes| QtWidgets.QMessageBox.No)
        event.ignore()

        if result == QtWidgets.QMessageBox.Yes:
            event.accept()
        """
        event.accept()


if __name__ == "__main__":
    import sys
    global voc2brain_app
    voc2brain_app = QtWidgets.QApplication(sys.argv)
    voc2brain_app.setOrganizationName("Voc2brain")
    voc2brain_app.setOrganizationDomain("voc2brain.sf.net")
    voc2brain_app.setApplicationName("voc2brain")
    voc2brain_app.setAttribute(10)

    mainWindow = MainWindow(voc2brain_app)
    mainWindow.show()
    sys.exit(app.exec_())