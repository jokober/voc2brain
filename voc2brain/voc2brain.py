#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time, sys, datetime
from database.database_table_definitions import Vocabulary_Table
from PyQt5 import QtCore, uic, QtWidgets

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from misc.custom_signals import Communicate
from tabs.init_main_window import init_main_window_class
from database.database_migrate import DatabaseMigrateClass
from dialogs.language_switcher import lsDialog

from misc.os_adjustments import os_adjustment_object
from misc.regular_db_tasks import RegularDBTasksClass

from tabs.configuration_tab import ConfigurationTabClass, ConfigManagerClass
from tabs.database_tab import DatabaseTabClass
from tabs.practice_tab import PracticeTabClass
from tabs.stats_tab import StatsTabClass
from tabs.course_tab import CourseTabClass
from tabs.add_card_tab import AddCardTab_class

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, voc2brain_app):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi(os.path.abspath(u'./ui_resources/MainWindow.ui'), self)

        self.version = "5.0beta"
        self.development_version = True


        #################
        # Get all custom signals
        #################
        self.communicate = Communicate()

        self.voc2brain_app = voc2brain_app

        #################
        # Create sqlalchemy engine and session
        #################
        self.local_engine = create_engine('sqlite:///'+ os_adjustment_object(self).database_path, isolation_level="READ UNCOMMITTED" )

        self.Session = sessionmaker(bind=self.local_engine)
        self.session = self.Session()

        from database.database_table_definitions import *
        self.base = Base
        self.base.metadata.create_all(self.local_engine, checkfirst=True)

        #################
        # Migrate database to newer version if applicable
        #################
        DatabaseMigrateClass(self).check_version()

        #################
        # Prepare the ui
        #################
        init_main_window_class(self)
        self.MainTabs.currentChanged.connect(self.whichTab)

        #################
        # Prepare config manager
        #################
        self.config = ConfigManagerClass(self)

        dict_of_ui_elements_and_config_keys = {
            "mainConfig/fontSize_feature": self.activate_fontsizeFeature,
            "mainConfig/window_reminder": self.own_window_radio,
            "mainConfig/notification_reminder": self.notification_radio,
            "mainConfig/design_feature": self.activate_Designs,
            "mainConfig/max_words": self.maxWordCount,
            "mainConfig/phase1": self.deck1_interval_lineedit,
            "mainConfig/phase2": self.deck2_interval_lineedit,
            "mainConfig/phase3": self.deck3_interval_lineedit,
            "mainConfig/phase4": self.deck4_interval_lineedit,
            "mainConfig/phase5": self.deck5_interval_lineedit,
            "mainConfig/phase6": self.deck6_interval_lineedit,
            "mainConfig/VocableReconsiderationKey": self.RandomVocConfigLine,
            "mainConfig/design_choice":self.design_combo,
            "mainConfig/font_size":self.fontsizecombo
        }

        for config_key in dict_of_ui_elements_and_config_keys:
            ui_element = dict_of_ui_elements_and_config_keys[config_key]
            self.config.add_config_handler(config_key, ui_element)

        #################
        #
        #################
        self.regular_db_tasks = RegularDBTasksClass(self)

    def whichTab(self):
        """

        Start the individual tab class if a tab button gets clicked

        """

        if self.MainTabs.currentIndex() == self.MainTabs.indexOf(self.stats_tab_page):
            StatsTabClass(self)
            self.checkVocs2learn()
        if self.MainTabs.currentIndex() == self.MainTabs.indexOf(self.practice_tab_page):
            self.seconds2 = time.time()
            self.flip_side_textedit.setFocus()
            PracticeTabClass(self)
        if self.MainTabs.currentIndex() == self.MainTabs.indexOf(self.database_tab_page):
            DatabaseTabClass(self).fill_table()
        if self.MainTabs.currentIndex() == self.MainTabs.indexOf(self.configuration_tab_page):
            self.config.get_config_dict()
            ConfigurationTabClass(self)
        if self.MainTabs.currentIndex() == self.MainTabs.indexOf(self.course_tab_page):
            CourseTabClass(self)
        if self.MainTabs.currentIndex() == self.MainTabs.indexOf(self.add_card_tab_page):
            AddCardTab_class(self)


    def checkVocs2learn(self):
        # leads to the amount of cards to learn for each day
        date = datetime.date.today()
        toLearnToday = self.session.query(Vocabulary_Table.card_id).filter(
             Vocabulary_Table.date_next_practice == date).count()
        return toLearnToday


    def translate_ui(self):
        """

        Loads the ui translations

        """
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
        """

        Event which will run as if the application gets closed

        """
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

def main():
    import sys
    global voc2brain_app
    voc2brain_app = QtWidgets.QApplication(sys.argv)
    voc2brain_app.setOrganizationName("Voc2brain")
    voc2brain_app.setOrganizationDomain("voc2brain.sf.net")
    voc2brain_app.setApplicationName("voc2brain")
    voc2brain_app.setAttribute(10)

    mainWindow = MainWindow(voc2brain_app)
    mainWindow.show()
    sys.exit(voc2brain_app.exec_())


if __name__ == "__main__":
    main()
