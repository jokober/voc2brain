# -*- coding: utf-8 -*-

import os, sys, codecs, webbrowser

from PyQt5 import QtCore, QtGui, uic, QtWidgets


operating_system = unicode(sys.platform) 

class lsDialog(QtWidgets.QDialog):
    def __init__(self, main_window):
        QtWidgets.QDialog.__init__(self)
        print os.getcwd()
        uic.loadUi(os.path.abspath(u'./ui_resources/language_switcher.ui'), self)

        self.translator_link.clicked.connect(self.open_translator_web)

        # Add languages to comboBox
        self.text_default = self.tr(u'Default')
        self.comboBox.addItem(self.text_default)
        self.comboBox.addItem(u'English')
        self.comboBox.addItem(u'German')
        self.comboBox.addItem(u'Spanish')
        self.comboBox.addItem(u'Turkish')
        self.comboBox.addItem(u'Greek')
        self.comboBox.addItem(u'Polish')
        self.comboBox.addItem(u'Arabic')
        self.comboBox.addItem(u'Thai')
        self.comboBox.addItem(u'French')
        
        #self.comboBox.addItem(u'Arabic')
        
        self.language = main_window.session.query(config_table).filter(config_table.key == "localization/LanguageKey")
        self.language = self.language.value
        print "#######################################################################"
        print "### Lamguage: " + unicode(self.language) + " ###"

        if self.language == u'no_translation':
            translation = u'English'
        elif self.language == u'es_ES':
            translation = u'Spanish'
        elif self.language == u'tr':
            translation = u'Turkish'
        elif self.language == u'de':
            translation = u'German'
        elif self.language == u'ar':
            translation = u'Arabic'
        elif self.language == u'el':
            translation = u'Greek'
        elif self.language == u'pl':
            translation = u'Polish'
        elif self.language == u'th_TH':
            translation = u'Thai'
        elif self.language == u'fr':
            translation = u'French'
            

        else:
            translation= self.text_default
                   
        self.comboBox.setCurrentIndex(self.comboBox.findText(translation))
        
        self.buttonBox.accepted.connect(self.changed_language)
        self.buttonBox.rejected.connect(self.close)
       
    def get_tr_file(self):
        translation = self.comboBox.currentText()
        
        if translation == u'German':
            tr_file = u'de'
        if unicode(translation) == u'Spanish':
            tr_file = u'es_ES'
        elif translation == u'Turkish':
            tr_file = u'tr'
        elif translation == u'English':
            tr_file= u'no_file'
        elif translation == u'Arabic':
            tr_file = u'ar'
        elif translation == u'Greek':
            tr_file = u'el'
        elif translation == u'Polish':
            tr_file = u'pl'
        elif translation == u'Thai':
            tr_file = u'th_TH'
        elif translation == u'French':
            tr_file = u'fr'
        else:
            tr_file= u'no_file'
        print "### TR File: " + unicode(tr_file) + " ###"
        return tr_file
        
    def changed_language(self):
        print 'Save localization ...'
        tr_file = self.get_tr_file()

        main_window.session.query(config_table).filter(config_table.key == "localization/LanguageKey").update({'value': unicode(tr_file)})
        main_window.session.commit()
        
        info = QtGui.QMessageBox(QtGui.QMessageBox.Information, u"Restart", "Please restart Voc2brain ...")
        info.exec_()
        
        self.close()
        
    def open_translator_web(self):
        webbrowser.open_new_tab("https://www.transifex.com/projects/p/Voc2brain/") 
        
