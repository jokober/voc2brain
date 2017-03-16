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

        # initiate config manager
        self.config_manager = config.ConfigManager(self.main_window)

        # load saved configurations
        self.load_config()

        self.main_window.communicate.config_updated.connect(lambda: self.save_config_to_db())

    def save_config_to_db(self):
        """
        Saves the current configurations in Config Manager to the database
        """
        print "### Info ### Save confic dict to db"
        print unicode(bool(1))
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


class ConfigurationTabClass(object):
    def __init__(self, main_window):
        self.main_window = main_window

        # Get a dictionary with all config keys and default values
        self.key_dictionary = self.get_key_dictionary()

        # Check if all configuration keys are saved in the database
        self.check_existence_of_configkeys()

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

    # Loads the design based on the saved settings
    def load_design(self):
        config_dict = ConfigDictClass(self.main_window).get_config_dict()
        if config_dict["mainConfig/design_feature"] == "False":
            self.main_window.design_combo.setCurrentIndex(self.main_window.design_combo.findText("Default"))
            self.main_window.activate_Designs.setChecked(False)
            self.main_window.designFrame.hide()
            return


        else:
            self.main_window.activate_Designs.setChecked(True)
            self.main_window.designFrame.show()


        list_of_styles = [
            ("Windows","windowsvista", ["win32"]),
            ("Plastique", "plastique", ["win32", 'linux2']),
            ("Fusion", "fusion", ["win32", 'linux2']),
            ("gtk", "gtk", ['linux2']),

        ]

        # clear design_combo and add default option
        self.main_window.design_combo.clear()
        self.main_window.design_combo.addItem(u'Default')
        self.main_window.applydesign_button.clicked.connect(partial(self.save_config,"mainConfig/design_choice"))

        load_design = ""
        for design_name, style_string, platforms in list_of_styles:
            print design_name
            print style_string
            print platforms

            if os_adjustment_object.operating_system in platforms:
                print 'OS JAAA'
                # fill combobox with course_names
                self.main_window.design_combo.addItem(design_name)
                print config_dict["mainConfig/design_choice"]
                print design_name


                # check
                if config_dict["mainConfig/design_choice"] == design_name:
                    load_design = style_string
                    self.main_window.design_combo.setCurrentIndex(self.main_window.design_combo.findText(design_name))

        print load_design
        # Apply design
        if load_design != "":
            self.main_window.voc2brain_app.setStyle(QtWidgets.QStyleFactory.create(load_design))
            self.main_window.voc2brain_app.setPalette(QtWidgets.QApplication.style().standardPalette())
        else:
            print "### Warning ### Design changed to default design"
            self.main_window.design_combo.setCurrentIndex(self.main_window.design_combo.findText("Default"))


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


    # Resets all settings to default
    def default_settings(self):
        # Get a dictionary with all config keys and default values
            print "### Warning ### Reset all configurations to default"
            for config in self.main_window.session.query(Config_Table).all():
                config.value = self.key_dictionary[config.key]
            self.main_window.session.commit()

    # Checks wheather all configurations are saved in the database
    def check_existence_of_configkeys(self):
        print "###################################################################################"
        for key_string in self.key_dictionary:
            if not self.main_window.session.query(Config_Table).filter_by(key=key_string).count():
                print "### Warning ### Following configKey can't be found in the 'config_table':" + unicode(key_string)
                print "                The configuration will be created with default value"
                self.main_window.session.add(Config_Table(key=key_string, value = self.key_dictionary[key_string]))
            self.main_window.session.commit()

    # Returns a dictionary with all configuration keys and their default value
    def get_key_dictionary(self):
        return {
            "mainConfig/Voc2brain_identification": unicode(random.randrange(1, 2344355)),
            "mainConfig/organise_lessons_feature": "False",
            "mainConfig/user_feature": "False",
            "mainConfig/backup_path": unicode(os_adjustment_object.backup_dirs),
            "mainConfig/design_feature": "False",
            "mainConfig/design_choice": "fusion",
            "mainConfig/reminder": "True",
            "mainConfig/fontSize_feature": "False",
            "mainConfig/font_size": "14",
            "mainConfig/notification_reminder": "False",
            "mainConfig/max_words": "0",
            "mainConfig/phase1": "0",
            "mainConfig/phase2": "3",
            "mainConfig/phase3": "12",
            "mainConfig/phase4": "30",
            "mainConfig/phase5": "90",
            "mainConfig/phase6": "120",
            'mainConfig/VocableReconsiderationKey': "2",
            "mainConfig/window_reminder": "True",
            "mainConfig/max_words": "60",
            "localization/ui_translation_language": "",
        }


"""        # Check if "font size feature" is activated and load ui-elements accordingly
        if bool(config_dict["mainConfig/fontSize_feature"]) == True:
            # self.main_window.size_frame.show()
            self.set_font_size(size=int(config_dict["mainConfig/font_size"]))

        else:
            self.main_window.size_frame.hide()
            self.set_font_size(size=14)










        # check if design configurations have been changed - load design if so
        if key == "mainConfig/design_feature" or key == "mainConfig/design_choice":
            # Load design
            self.load_design()"""