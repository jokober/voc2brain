from PyQt5 import QtGui, QtCore, uic, QtWidgets
import os
from misc.os_adjustments import os_adjustment_object


# LOAD, REFRESH AND CONNECT UI ELEMENTS
class init_main_window_class(object):
    def __init__(self, main_window):
        self.main_window = main_window

        self.init_ui_elememts()

    def init_ui_elememts(self):
        #############################
        # Start Tab: Load icons, connect signals and initiate ui elements in the "Start Tab"
        #############################
        self.main_window.MainTabs.setTabIcon(self.main_window.MainTabs.indexOf(self.main_window.stats_tab_page), QtGui.QIcon(os.path.join(os.path.abspath(u'.'), U'icons/tab_start.svg')))

        #############################
        # Practice Tab: Load icons, connect signals and initiate ui elements in the "Practice Tab"
        #############################
        self.main_window.MainTabs.setTabIcon(self.main_window.MainTabs.indexOf(self.main_window.practice_tab_page), QtGui.QIcon(os.path.join(os.path.abspath(u'.'), U'icons/tab_interrogation.svg')))

        #############################
        # New Word Tab: Load icons, connect signals and initiate ui elements in the "New Word Tab"
        #############################
        self.main_window.MainTabs.setTabIcon(self.main_window.MainTabs.indexOf(self.main_window.add_card_tab_page), QtGui.QIcon(os.path.join(os.path.abspath(u'.'), u'icons/tab_add.svg')))

        #############################
        # Database Tab: Load icons, connect signals and initiate ui elements in the "Database Tab"
        #############################
        self.main_window.MainTabs.setTabIcon(self.main_window.MainTabs.indexOf(self.main_window.database_tab_page), QtGui.QIcon(os.path.join(os.path.abspath(u'.'), U'icons/tab_list.svg')))

        #############################
        # Database Tab: Load icons, connect signals and initiate ui elements in the "Database Tab"
        #############################
        self.main_window.MainTabs.setTabIcon(self.main_window.MainTabs.indexOf(self.main_window.course_tab_page),
                                     QtGui.QIcon(os.path.join(os.path.abspath(u'.'), U'icons/tab_courses_grey_2.svg')))

        #############################
        # Configuration Tab: Load icons, connect signals and initiate ui elements in the "Configuration Tab"
        #############################
        self.main_window.MainTabs.setTabIcon(self.main_window.MainTabs.indexOf(self.main_window.configuration_tab_page), QtGui.QIcon(os.path.join(os.path.abspath(u'.'), u'icons/tab_conf.svg')))

        Tablist = [
        (self.main_window.SettingsTab_flashcard, QtGui.QIcon(os.path.join(os.path.abspath(u'.'), U'icons/tab_flashcardConfig.svg'))),
        (self.main_window.SettingsTab_reminder, QtGui.QIcon(os.path.join(os.path.abspath(u'.'), U'icons/tab_reminder.svg'))),
        #(self.main_window.SettingsTab_synchronisation, QtGui.QIcon(os.path.join(os.path.abspath(u'.'), U'icons/tab_sync.svg'))),
        (self.main_window.SettingsTab_backups, QtGui.QIcon(os.path.join(os.path.abspath(u'.'), U'icons/tab_backup.svg'))),
        (self.main_window.SettingsTab_features , QtGui.QIcon(os.path.join(os.path.abspath(u'.'), U'icons/tab_features.svg'))),

        ]
        for tab in Tablist:
            tab[0].setIcon(tab[1])


        self.main_window.notification_icon_label.setPixmap(
            QtGui.QPixmap(os.path.join(os.path.abspath(u'.'), os.path.normcase(u"icons/notify.png"))))
        self.main_window.window_icon_label.setPixmap(
            QtGui.QPixmap(os.path.join(os.path.abspath(u'.'), os.path.normcase(u"icons/fenster.png"))))
        self.main_window.LevelPictureLabel.setPixmap(
            QtGui.QPixmap(os.path.join(os.path.abspath(u'.'), os.path.normcase(u"icons/LevelPicture.png"))))

        self.main_window.maxWordCount.setValidator(QtGui.QIntValidator(0, 999, self.main_window))
        self.main_window.deck1_interval_lineedit.setValidator(QtGui.QIntValidator(0, 999, self.main_window))
        self.main_window.deck2_interval_lineedit.setValidator(QtGui.QIntValidator(0, 999, self.main_window))
        self.main_window.deck3_interval_lineedit.setValidator(QtGui.QIntValidator(0, 999, self.main_window))
        self.main_window.deck4_interval_lineedit.setValidator(QtGui.QIntValidator(0, 999, self.main_window))
        self.main_window.deck5_interval_lineedit.setValidator(QtGui.QIntValidator(0, 999, self.main_window))
        self.main_window.deck6_interval_lineedit.setValidator(QtGui.QIntValidator(0, 999, self.main_window))
        self.main_window.RandomVocConfigLine.setValidator(QtGui.QIntValidator(0, 999, self.main_window))

        Featurelist = [
            (self.main_window.activate_Designs, QtGui.QIcon(os.path.join(os.path.abspath(u'.'), U'icons/feature_design.svg')),
             "mainConfig/design_feature"),
            (self.main_window.activate_fontsizeFeature, QtGui.QIcon(os.path.join(os.path.abspath(u'.'), U'icons/feature_font.svg')),
             "mainConfig/fontSize_feature"),
        ]

        for feature in Featurelist:
            feature[0].setIcon(feature[1])


        list_of_styles = [
            ("windowsvista", ["win32"]),
            ("plastique", ["win32", 'linux2']),
            ("fusion", ["win32", 'linux2']),
            ("gtk", ['linux2'])]

        # clear design_combo and add default option
        self.main_window.design_combo.clear()
        self.main_window.design_combo.addItem(u'Default')

        for style_string, platforms in list_of_styles:
            if os_adjustment_object(self.main_window).operating_system in platforms:
                # fill combobox with course_names
                self.main_window.design_combo.addItem(style_string)



        ######################
        # OS specific changes to the ui
        ######################
        if os_adjustment_object(self.main_window).operating_system == 'linux2':
            pass
        elif os_adjustment_object.operating_system == "darwin":
            self.main_window.activate_Designs.hide()
            self.main_window.line_12.hide()
        elif os_adjustment_object.operating_system == 'win32':
            pass











