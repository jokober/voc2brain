# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore, QtWidgets
import random, webbrowser
from functools import partial

from misc.os_adjustments import os_adjustment_object
from misc.backup_database import BackupDatabaseClass

from dialogs.about_dialog import aboutDialog

from database.database_table_definitions import Vocabulary_Table, Deleted_Vocabulary_Table, Config_Table, Metadata_Table, Activity_Table
from sqlalchemy import Table
import time

class ConfigDictClass(object):
    def __init__(self, main_window):
        self.main_window = main_window

    def get_config_dict(self):
        config_dict = {}
        for row in self.main_window.session.query(Config_Table).all():
            config_dict[row.key] = row.value

        return config_dict

class ConfigurationTabClass(object):
    def __init__(self, main_window):
        self.main_window = main_window

        # Get a dictionary with all config keys and default values
        self.key_dictionary = self.get_key_dictionary()

        # Check if all configuration keys are saved in the database
        self.check_existence_of_configkeys()

        # Run function which creates the connections in the "configuration_tab"
        self.create_pyqt_connections()

        # Connect the settings buttons to the individual page
        self.main_window.SettingsTab_flashcard.pressed.connect(lambda: self.main_window.configTabs.setCurrentIndex(0))
        self.main_window.SettingsTab_reminder.pressed.connect(lambda: self.main_window.configTabs.setCurrentIndex(1))
        self.main_window.SettingsTab_backups.pressed.connect(lambda: BackupDatabaseClass(self.main_window))
        self.main_window.SettingsTab_features.pressed.connect(lambda: self.main_window.configTabs.setCurrentIndex(4))

        # Connections in Settings
        self.main_window.reset_config_button.clicked.connect(lambda: self.default_settings())
        self.main_window.about_button.clicked.connect(self.show_aboutDialog)
        self.main_window.report_problem_button.clicked.connect(lambda: webbrowser.open_new_tab("http://voc2brain.sourceforge.net/?page_id=141"))
        #self.main_window.communicate.reload_config_ui_signal.connect(lambda: self.reload_config_ui_elements())

        self.reload_config_ui_elements()

    def show_aboutDialog(self):
        self.aboutDialog = aboutDialog()
        self.aboutDialog.show()

    # UPDATES CONFIG UI-ELEMENTS BASED ON THE KEY
    def reload_config_ui_elements(self):
        config_dict = ConfigDictClass(self.main_window).get_config_dict()


        print 'BLAAAAA loaaad  ' + str(self.main_window.activate_fontsizeFeature.isChecked())

        #

        #  save settings (all checkbox ui elements)

        for key in ["mainConfig/fontSize_feature","mainConfig/organise_lessons_feature", "mainConfig/window_reminder","mainConfig/notification_reminder","mainConfig/design_feature"]:

            if key =="mainConfig/fontSize_feature":
                self.main_window.activate_fontsizeFeature.setChecked(bool(config_dict[key]))
            if key =="mainConfig/organise_lessons_feature":
                self.main_window.activate_organise_lessons_feature.setChecked(bool(config_dict[key]))
            if key =="mainConfig/window_reminder":
                self.main_window.own_window_radio.setChecked(bool(config_dict[key]))
            if key =="mainConfig/notification_reminder":
                self.main_window.notification_radio.setChecked(bool(config_dict[key]))
            if key =="mainConfig/design_feature":
                self.main_window.activate_Designs.setChecked(bool(config_dict[key]))

        #    print key + str(config_dict[key])
        #    self.get_checkbox_config_ui_elements()[key]

        for key in self.get_textedit_config_ui_elements():
            # save settings (all textedit/lineedit ui elements)
            self.get_textedit_config_ui_elements()[key].setText(unicode(config_dict[key]))


        # Check if "font size feature" is activated and load ui-elements accordingly
        if bool(config_dict["mainConfig/fontSize_feature"]) == True:
            self.main_window.size_frame.show()
            self.set_font_size(size = int(config_dict["mainConfig/font_size"]))

        else:
            self.main_window.size_frame.hide()
            self.set_font_size(size = 14)

        '''
        if self.main_window.MainTabs.currentIndex() == self.main_window.MainTabs.indexOf(self.main_window.configuration_tab_page):
            self.search_delay = QtCore.QTimer()
            self.search_delay.timeout.connect(lambda: self.reload_config_ui_elements())
            self.search_delay.setSingleShot(True)
            self.search_delay.start(800)
            '''

    def save_config(self, key):
        # save settings (all checkbox ui elements)
        "mainConfig/fontSize_feature": self.main_window.activate_fontsizeFeature,
        "mainConfig/organise_lessons_feature": self.main_window.activate_organise_lessons_feature,
        "mainConfig/window_reminder": self.main_window.own_window_radio,
        "mainConfig/notification_reminder": self.main_window.notification_radio,
        "mainConfig/design_feature":self.main_window.activate_Designs,

        if key in self.get_checkbox_config_ui_elements():
            new_value = unicode(self.get_checkbox_config_ui_elements()[key].isChecked())
            self.main_window.session.query(Config_Table).filter_by(key=key).update({'value': new_value})

            print 'Save   ' + key +str(self.main_window.activate_fontsizeFeature.isChecked())

        # save settings (all textedit/lineedit ui elements)
        if key in self.get_textedit_config_ui_elements():
            new_value = unicode(self.get_textedit_config_ui_elements()[key].text())
            self.main_window.session.query(Config_Table).filter_by(key=key).update({'value': new_value})



        # commit to database
        self.main_window.session.commit()

        # check if design configurations have been changed - load design if so
        if key == "mainConfig/design_feature" or key == "mainConfig/design_choice":
            # save design choice
            new_value = unicode(self.main_window.design_combo.currentText())
            self.main_window.session.query(Config_Table).filter_by(key="mainConfig/design_choice").update(
                {'value': new_value})


            # Load design
            self.load_design()

        print "### Info ### Saving following configuration: " + key + "New Value: " + new_value

        self.reload_config_ui_elements()

    def create_pyqt_connections(self):
        for key in self.get_checkbox_config_ui_elements():
            self.get_checkbox_config_ui_elements()[key].stateChanged.connect(partial(self.save_config, key))

        for key in self.get_textedit_config_ui_elements():
            self.get_textedit_config_ui_elements()[key].textChanged.connect(partial(self.save_config, key ))

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

    def get_checkbox_config_ui_elements(self):
        return {
            "mainConfig/fontSize_feature": self.main_window.activate_fontsizeFeature,
            "mainConfig/organise_lessons_feature": self.main_window.activate_organise_lessons_feature,
            "mainConfig/window_reminder": self.main_window.own_window_radio,
            "mainConfig/notification_reminder": self.main_window.notification_radio,
            "mainConfig/design_feature":self.main_window.activate_Designs,
        }

    def get_textedit_config_ui_elements(self):
        return {
            "mainConfig/max_words":self.main_window.maxWordCount,
            "mainConfig/phase1":self.main_window.deck1_interval_lineedit,
            "mainConfig/phase2":self.main_window.deck2_interval_lineedit,
            "mainConfig/phase3":self.main_window.deck3_interval_lineedit,
            "mainConfig/phase4":self.main_window.deck4_interval_lineedit,
            "mainConfig/phase5":self.main_window.deck5_interval_lineedit,
            "mainConfig/phase6":self.main_window.deck6_interval_lineedit,
            "mainConfig/VocableReconsiderationKey":self.main_window.RandomVocConfigLine

        }