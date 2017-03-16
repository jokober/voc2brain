# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore, QtWidgets
import random, webbrowser
from functools import partial
from pyqtconfig import config

from misc.os_adjustments import os_adjustment_object
from misc.backup_database import BackupDatabaseClass

from dialogs.about_dialog import aboutDialog

from database.database_table_definitions import Vocabulary_Table, Deleted_Vocabulary_Table, Config_Table, Metadata_Table, Activity_Table
from sqlalchemy import Table

class ConfigManagerClass(object):
    def __init__(self, main_window):
        self.main_window = main_window

        # Get key dictionary
        self.key_dictionary = self.get_key_dictionary()

        # Check existance of all config keys
        self.check_existence_of_configkeys()

        # initiate config manager
        self.config_manager = config.ConfigManager(self.main_window)

        # load saved configurations
        self.load_config()

        self.main_window.communicate.config_updated.connect(lambda: self.config_changed())

    def config_changed(self):
        """
        This fuction will run as soon as a config has been changed
        """
        ConfigSpecific_UiChanges(self.main_window)
        self.save_config_to_db()

    def save_config_to_db(self):
        """
        Saves the current configurations in Config Manager to the database
        """

        print "### Info ### Save config dict to db"

        config_dict = self.get_config_dict()
        for config_key in config_dict:
            self.main_window.session.query(Config_Table).filter_by(key=config_key).update({'value': config_dict[config_key]})
        self.main_window.session.commit()

    def get_config_dict(self):
        """
        Returns a dict with the current configurations
        """
        print self.config_manager.as_dict()
        return self.config_manager.as_dict()

    def load_config(self):
        """
        Loads the configurations from database and loads them into the Config Manager
        """
        config_dict = {}
        for row in self.main_window.session.query(Config_Table).all():
            config_dict[row.key] = row.value

        self.config_manager.set_defaults(config_dict)

    def get(self, config_key):
        """
        Returns the value of a config_key
        """
        return self.config_manager.get(config_key)

    def set(self, config_key, value):
        """
        Sets the config to a new value. The UI-elements will change their status accordingly.
        Save the new settings to the database.
        """
        self.config_manager.set(config_key, value)

        self.save_config_to_db()
        
    def add_config_handler(self,config_key, ui_element):
        self.config_manager.add_handler(config_key, ui_element)

    def default_settings(self):
        """
        Get a dictionary with all config keys and default values

        """
        print "### Warning ### Reset all configurations to default"
        self.config_manager.set_defaults(self.get_key_dictionary)

    def check_existence_of_configkeys(self):
        '''

        Checks wheather all configurations are saved in the database

        '''
        for key_string in self.key_dictionary:
            if not self.main_window.session.query(Config_Table).filter_by(key=key_string).count():
                print "### Warning ### Following configKey can't be found in the 'config_table':" + unicode(key_string)
                print "                The configuration will be created with default value"
                self.main_window.session.add(Config_Table(key=key_string, value=self.key_dictionary[key_string]))
            self.main_window.session.commit()

    def get_key_dictionary(self):
        '''
        Returns a dictionary with all configuration keys and their default value

        '''
        return {
            "mainConfig/organise_lessons_feature": "1",
            "mainConfig/user_feature": "1",
            "mainConfig/backup_path": unicode(os_adjustment_object.backup_dirs),
            "mainConfig/design_feature": "1",
            "mainConfig/design_choice": "fusion",
            "mainConfig/reminder": "0",
            "mainConfig/fontSize_feature": "1",
            "mainConfig/font_size": "14",
            "mainConfig/notification_reminder": "0",
            "mainConfig/max_words": "0",
            "mainConfig/phase1": "0",
            "mainConfig/phase2": "3",
            "mainConfig/phase3": "12",
            "mainConfig/phase4": "30",
            "mainConfig/phase5": "90",
            "mainConfig/phase6": "120",
            'mainConfig/VocableReconsiderationKey': "2",
            "mainConfig/window_reminder": "1",
            "mainConfig/max_words": "60",
            "localization/ui_translation_language": "",
        }

class ConfigSpecific_UiChanges(object):
    def __init__(self, main_window):
        self.main_window = main_window

        # Check if "font size feature" is activated and load ui-elements accordingly

        print self.main_window.config.get("mainConfig/fontSize_feature")
        if self.main_window.config.get("mainConfig/fontSize_feature") == True:
            self.main_window.size_frame.show()
            self.set_font_size(size=int(self.main_window.config.get("mainConfig/font_size")))

        else:
            self.main_window.size_frame.hide()
            self.set_font_size(size=14)

        if self.main_window.config.get("mainConfig/design_feature") == True:
            self.main_window.designFrame.show()
            if not self.main_window.design_combo.currentText() == "Default":
                self.main_window.voc2brain_app.setStyle(
                    QtWidgets.QStyleFactory.create(self.main_window.design_combo.currentText()))
                self.main_window.voc2brain_app.setPalette(QtWidgets.QApplication.style().standardPalette())
        else:
            self.main_window.designFrame.hide()

    # Sets the font size of multiple ui-elements based on the saved value
    def set_font_size(self, size):
        fontsize = QtGui.QFont()
        fontsize.setPointSize(size)

        list_of_ui_elements=[
            (self.main_window.front_input_textedit),
            (self.main_window.back_input_textedit),
            (self.main_window.front_side_textedit),
            (self.main_window.flip_side_textedit),
            (self.main_window.fontsizeline)
        ]

        for ui_element in list_of_ui_elements:
            ui_element.setFont(fontsize)

class ConfigurationTabClass(object):
    def __init__(self, main_window):
        self.main_window = main_window

        # Connect the settings buttons to the individual page
        self.main_window.SettingsTab_flashcard.pressed.connect(lambda: self.main_window.configTabs.setCurrentIndex(0))
        self.main_window.SettingsTab_reminder.pressed.connect(lambda: self.main_window.configTabs.setCurrentIndex(1))
        self.main_window.SettingsTab_backups.pressed.connect(lambda: BackupDatabaseClass(self.main_window))
        self.main_window.SettingsTab_features.pressed.connect(lambda: self.main_window.configTabs.setCurrentIndex(4))

        # Connections in Settings
        self.main_window.reset_config_button.clicked.connect(lambda: self.default_settings())
        self.main_window.about_button.clicked.connect(self.show_aboutDialog)
        self.main_window.report_problem_button.clicked.connect(lambda: webbrowser.open_new_tab("http://voc2brain.sourceforge.net/?page_id=141"))

    def show_aboutDialog(self):
        self.aboutDialog = aboutDialog()
        self.aboutDialog.show()










