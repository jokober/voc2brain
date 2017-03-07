# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore, QtWidgets
import random, webbrowser
from functools import partial

from misc.os_adjustments import os_adjustment_object
from misc.backup_database import BackupDatabaseClass

from dialogs.about_dialog import aboutDialog

from database.database_table_definitions import Vocabulary_Table, Deleted_Vocabulary_Table, Config_Table, Metadata_Table, Activity_Table
from sqlalchemy import Table

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
        self.main_window.communicate.reload_config_ui_signal.connect(lambda: self.reload_config_ui_elements())

        self.reload_config_ui_elements()

    def show_aboutDialog(self):
        self.aboutDialog = aboutDialog()
        self.aboutDialog.show()

    # Updates all ui-elements
    def reload_config_ui_elements(self):
        config_dict = ConfigDictClass(self.main_window)
        print type(config_dict)
        print config_dict

        # Load number of completed words to practice
        self.main_window.RandomVocConfigLine.setText(unicode(config_dict["mainConfig/completed_cards_to_practice"]))

        # Load number of maximum words to practice
        self.main_window.maxWordCount.setText(unicode(config_dict["mainConfig/max_words"]))

        # Check if "font size feature" is activated and load ui-elements accordingly
        if bool(config_dict["mainConfig/fontSize_feature"]) == True:
            self.main_window.activate_fontsizeFeature.setCheckState(QtCore.Qt.Checked)
            self.main_window.size_frame.show()
            self.set_font_size(size = int(config_dict["mainConfig/font_size"]))

        else:
            self.main_window.activate_fontsizeFeature.setChecked(False)
            self.main_window.size_frame.hide()
            self.set_font_size(size = 14)

        # Update the intval between decks
        self.main_window.deck1_interval_lineedit.setText(unicode(config_dict["mainConfig/phase1"]))
        self.main_window.deck2_interval_lineedit.setText(unicode(config_dict["mainConfig/phase2"]))
        self.main_window.deck3_interval_lineedit.setText(unicode(config_dict["mainConfig/phase3"]))
        self.main_window.deck4_interval_lineedit.setText(unicode(config_dict["mainConfig/phase4"]))
        self.main_window.deck5_interval_lineedit.setText(unicode(config_dict["mainConfig/phase5"]))
        self.main_window.deck6_interval_lineedit.setText(unicode(config_dict["mainConfig/phase6"]))

        # Load design
        self.load_design(value = config_dict["mainConfig/design_feature"])

        # Loads multiple languages configuration
        self.main_window.activate_organise_lessons_feature.setChecked(bool(config_dict["mainConfig/advanced_courses_feature"]))
        if bool(config_dict["mainConfig/advanced_courses_feature"]) == True:
            self.frame_9.show()
            self.language.show()
            self.comboBox.show()
        else:
            self.MainTabs.removeTab(self.MainTabs.indexOf(self.course_tab_page))
            self.frame_9.hide()
            self.language.hide()
            self.comboBox.hide()

        # Insert all course names to the "course_comboBox"
        self.main_window.course_comboBox.clear()
        for course in self.main_window.session.query(Courses_Table).all():
            if course.course_name == "":
                self.main_window.course_comboBox.addItem("Course")
            else:
                self.main_window.course_comboBox.addItem(course.course_name)

        # Load reminder checkBoxes
        self.main_window.own_window_radio.setChecked(bool(config_dict["mainConfig/window_reminder"]))
        self.main_window.notification_radio.setChecked(bool(config_dict["mainConfig/notification_reminder"]))

    def save_config(self, args):
        self.main_window.session.query(Config_Table).filter_by(key=args["key"]).update({'value': args["value"]})
        self.main_window.session.commit()

        self.reload_config_ui_elements()

    def create_pyqt_connections(self):
        list_of_checkbox_config_ui_elements = [
            (self.main_window.activate_fontsizeFeature,  "mainConfig/fontSize_feature"),
            (self.main_window.activate_organise_lessons_feature, "mainConfig/organise_lessons_feature"),
            (self.main_window.own_window_radio, "mainConfig/window_reminder"),
            (self.main_window.notification_radio, "mainConfig/notification_reminder"),
            (self.main_window.activate_Designs, "mainConfig/design_feature"),
        ]

        for ui_element, key in list_of_checkbox_config_ui_elements:
            args = {"key":key, "value": unicode(ui_element.isChecked())}
            ui_element.clicked.connect(partial(self.save_config, args))


            list_of_textedit_config_ui_elements =[
                (self.main_window.maxWordCount, "mainConfig/max_words"),
                (self.main_window.deck1_interval_lineedit,"mainConfig/phase1"),
                (self.main_window.deck2_interval_lineedit, "mainConfig/phase2"),
                (self.main_window.deck3_interval_lineedit, "mainConfig/phase3"),
                (self.main_window.deck4_interval_lineedit, "mainConfig/phase4"),
                (self.main_window.deck5_interval_lineedit, "mainConfig/phase5"),
                (self.main_window.deck6_interval_lineedit, "mainConfig/phase6"),
                (self.main_window.RandomVocConfigLine,"mainConfig/VocableReconsiderationKey"),

            ]
            for ui_element, key in list_of_textedit_config_ui_elements:
                args = {"key":key, "value": unicode(ui_element.text())}
                ui_element.editingFinished.connect(partial(self.save_config, args))


    # Loads the design based on the saved settings
    def load_design(self, value):
        if bool(value) == False:
            self.main_window.design_combo.setCurrentIndex(self.main_window.design_combo.findText("Default"))
            stylesheetFile = False
            self.main_window.activate_Designs.setChecked(False)
            self.designFrame.hide()

        else:
            self.main_window.activate_Designs.setChecked(True)
            self.designFrame.show()

            if value == "Green":
                self.main_window.design_combo.setCurrentIndex(self.main_window.design_combo.findText("Green"))
                stylesheetFile = os_adjustment_object.stylesheet_green
            elif value == "Plastique":
                self.main_window.design_combo.setCurrentIndex(self.main_window.design_combo.findText("Plastique"))
                app.setStyle(QtWidgets.QStyleFactory.create("plastique"))
                app.setPalette(QtWidgets.QApplication.style().standardPalette())

                stylesheetFile = os_adjustment_object.stylesheet_plastique
            elif value == "Windows":
                self.main_window.design_combo.setCurrentIndex(self.main_window.design_combo.findText("Windows"))
                app.setStyle(QtWidgets.QStyleFactory.create("windowsvista"))
                app.setPalette(QtWidgets.QApplication.style().standardPalette())

                stylesheetFile = os_adjustment_object.stylesheet_general
            elif value == "Pink":
                self.main_window.design_combo.setCurrentIndex(self.main_window.design_combo.findText("Pink"))
                stylesheetFile = os_adjustment_object.stylesheet_pink

            else:
                self.main_window.design_combo.setCurrentIndex(self.main_window.design_combo.findText("Default"))
                stylesheetFile = False

            if stylesheetFile != False:
                self.main_window.setStylesheet(stylesheetFile)

            else:
                if os_adjustment_object.operating_system == 'linux2':
                    app.setStyle(QtWidgets.QStyleFactory.create("gtk"))
                    app.setPalette(QtWidgets.QApplication.style().standardPalette())

                    self.main_window.setStylesheet(os_adjustment_object.stylesheet_general)
                elif os_adjustment_object.operating_system == 'win32':
                    # app.setStyle(QtWidgets.QStyleFactory.create("plastique"))
                    app.setPalette(QtWidgets.QApplication.style().standardPalette())

                    self.main_window.setStylesheet(os_adjustment_object.stylesheet_plastique)

                self.main_window.hide_design()

    # Sets the font size of multiple ui-elements based on the saved value
    def set_font_size(self, size):
        fontsize = QtGui.QFont()
        fontsize.setPointSize(size)

        self.main_window.fontsizeline.setFont(fontsize)
        self.main_window.vorderseite_eingabe.setFont(fontsize)
        self.main_window.rueckseite_eingabe.setFont(fontsize)
        self.main_window.front_side_textedit.setFont(fontsize)
        self.main_window.flip_side_textedit.setFont(fontsize)
        self.main_window.fontsizeline.setFont(fontsize)

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
            "mainConfig/completed_cards_to_practice": "2",
            "mainConfig/window_reminder": "True",
            "mainConfig/max_words": "60",
            "localization/ui_translation_language": "",
        }


