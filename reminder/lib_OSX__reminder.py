# -*- coding: utf-8 -*-

"""\
Name:		Voc2brain
Author:		Jonathan Kossick (Germany)
Description: Voc2brain is an free and open-source vocabulary program for Windows, Linux and Mac.
Summary: Contains the notification and reminder functions

You may use Voc2brain under the terms of either the BSD License or the GNU General Public License (GPL) Version 3.

You don't have to do anything special to choose one license or the other and you don't have to notify anyone which license you are using. You are free to use Voc2brain in commercial projects as long as the copyright header is left intact.
Copyright (C) 2010-2014  Jonathan Kossick <dev.kossick@googlemail.com>

GPL License:
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
BSD License:
    
    The Regents of the University of California. All rights reserved.
    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
    Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
    All advertising materials mentioning features or use of this software must display the following acknowledgement: "This product includes software developed by the University of California, Berkeley and its contributors."
    Neither the name of the University nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
    THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

import sys, os, datetime, configurations.configurations, time, codecs
from database import Voc2brainDatabaseClass

#path =  os.path.abspath("..")+'/database'
#sys.path.append(path)
import database.database
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
from localization.language_switcher_start import lsDialog

date_today = datetime.date.today() 

operating_system = unicode(sys.platform)
#Get path for database
#check os
if operating_system == 'linux2':
        workplace = os.path.abspath(os.path.expanduser(u'~')+u'/.voc2brain')
        FILENAME =  os.path.abspath(os.path.expanduser(u'~')+u'/.voc2brain/vocabulary.sdb3')
    
elif operating_system =="darwin":
    workplace = os.path.abspath(os.path.expanduser(u'~')+u'/Library/Application Support/voc2brain')
    FILENAME =  os.path.abspath(workplace+u'/vocabulary.sdb3')

elif operating_system == 'win32':
    workplace = os.path.join(os.environ[u'APPDATA'], os.path.normcase(u"voc2brain"))
    FILENAME =  os.path.join(os.environ[u'APPDATA'], os.path.normcase(u'voc2brain/vocabulary.sdb3'))
        
icon = QtGui.QIcon(os.path.join(os.path.abspath(u'.'), u'icons/voc2brain_icon.svg'))
start_file=os.path.join(workplace, "start.txt")


appSettings=Voc2brainDatabaseClass(FILENAME)


app = QtGui.QApplication(sys.argv) 

translator = QtCore.QTranslator()
lsDialog(appSettings)
print lsDialog(appSettings).get_tr_file() + "Language settings when loading"
if lsDialog(appSettings).get_tr_file() != 'no_file':
    print "[Use translation file]"
    translator.load(lsDialog(appSettings).get_tr_file() + '.qm', './translation/')
elif lsDialog(appSettings).get_tr_file() == 'no_translation': 
    print "[Use no translation]"
    pass
else:
    print "[Use system language]"
    if QtCore.QLocale.system().name().split('_')[0]!='en':
        translator.load(u'voc2brain_' + QtCore.QLocale.system().name().split('_')[0] + '.qm', './translation/')
app.installTranslator(translator)

QtCore.QTextCodec.setCodecForTr(QtCore.QTextCodec.codecForName("UTF-8"))




#class SystemTrayIcon(QtGui.QSystemTrayIcon):
#
#    def __init__(self, icon, parent=None):
#        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
#        menu = QtGui.QMenu(parent)
#        self.exitAction = menu.addAction("Exit")
#        self.exitAction.triggered.connect(self.hide)
#        self.setContextMenu(menu)

class TriggerReminderClass(QtGui.QDialog): 
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.appSettings=self
        
        # --> Start Database class
        self.Voc2brainDatabase = Voc2brainDatabaseClass(FILENAME)
        self.getWordsToday()
        
            
        # --> Update VocabularyToday Timeout
        self.updateTimer=QtCore.QTimer()
        self.updateTimer.timeout.connect(self.getWordsToday)
        self.updateTimer.start(10800000)
        
        self.Voc2brainDatabase.startSynchronization()
        # --> Synchronize Timeout
        self.syncTimer=QtCore.QTimer()
        self.syncTimer.timeout.connect(self.Voc2brainDatabase.startSynchronization)
        self.syncTimer.start(10800000)                     
            
    def getWordsToday(self):
        self.vocTotal=0
        #self.User1_vocTotal = 0
        #self.User2_vocTotal = 0
        #self.User3_vocTotal = 0
        #self.User4_vocTotal = 0
        #self.User5_vocTotal = 0
        
        users=[1,2,3,4,5]
        for user in users:
            vocab = self.Voc2brainDatabase.select_voc_for_interrogation(date_today, user)
            self.vocTotal=self.vocTotal + len(vocab)
            
            if user==1:
                self.User1_vocTotal = len(vocab)
            elif user==2:
                self.User2_vocTotal =len(vocab) 
            elif user==3:
                self.User3_vocTotal = len(vocab)
            elif user==4:
                self.User4_vocTotal =len(vocab)
            elif user==5:
                self.User5_vocTotal =  len(vocab)
                
            
            self.maxWords=appSettings.value("mainConfig/maxWordCount","80")[0]
            if self.vocTotal > self.maxWords and self.maxWords != 0:
                self.Voc2brainDatabase.changeDateTomorrow(self.vocTotal, self.maxWords, user)
                print "### Max words - Change Dates ###"
                
                print "Available words:" + unicode(self.vocTotal)
                    
   
        if self.vocTotal != 0:

            if erinnern == 'yes' and notifikations == 'yes':
                self.showNotification()
                    
                self.timer=QtCore.QTimer()
                self.timer.timeout.connect(self.getWordsToday)
                self.timer.start(10000000)
                    
            if erinnern == 'yes' and w_notify == 'yes':
                self.ReminderWindow()

                
        
    def showNotification(self):
        self.text2 = unicode(app.tr('You should learn some vocabularies... '))
        self.text1 = unicode(app.tr("Available words:")+" "+unicode(self.vocTotal))
        
        if operating_system =="linux2":
            print "Notify"
            
            import pynotify
            pynotify.init("Basics")
            
            n = pynotify.Notification(self.text2, self.text1)
            n.show()
                    
        elif operating_system =="win32":
            self.trayIcon=SystemTrayIcon(icon)
            self.trayIcon.show()
            self.trayIcon.showMessage(self.text2,self.text1)
            self.trayIcon.messageClicked.connect(self.start_vtb)
            time.sleep(15)
            self.trayIcon.hide()
            
        if operating_system == "darwin":
            print "### Show OS X Notification ... ###"
            from pync import Notifier
            Notifier.notify(self.text1, title=self.text2)
            

    def start_vtb(self):
        print "Start Voc2brain ..."
        self.hide()
        if operating_system =="linux2":
            os.system("python gui_starter.py")
        elif operating_system =="win32":
            os.system("gui_starter.exe")
        elif operating_system =="darwin":
            pass
             
    def ReminderWindow(self):
        print "### Show Window ... ###"
        uic.loadUi('erinnerung.ui', self)
        self.setWindowTitle(unicode(self.tr('Reminder')))
        
        self.User1_reminderLabel.hide()
        self.User2_horizontalLayout.hide()
        self.User3_horizontalLayout.hide()
        self.User4_horizontalLayout.hide()
        self.User5_horizontalLayout.hide()


        self.dont_remember.stateChanged.connect(self.dont_remember_anymore)                
        self.setWindowIcon(icon)
        
        if appSettings.value("mainConfig/userFeatureKey", "1") == 1:
            
            self.User1_reminderLabel.show()
            self.number_voc.setText(str(self.User1_vocTotal))
            if appSettings.value("userFeature/User1Key", "")  !="":
                self.User1_reminderLabel.setText(str(appSettings.value("userFeature/User1Key", "")))
                
            if self.User2_vocTotal != 0:
                self.User2_number_voc.setText(str(self.User2_vocTotal))
                self.User2_horizontalLayout.show()                
                if appSettings.value("userFeature/User2Key", "")  !="":
                    self.User2_reminderLabel.setText(str(appSettings.value("userFeature/User2Key", "")))
                    
            if self.User3_vocTotal != 0:
                self.User3_number_voc.setText(str(self.User3_vocTotal))
                self.User3_horizontalLayout.show()                
                if appSettings.value("userFeature/User3Key", "")  !="":
                    self.User3_reminderLabel.setText(str(appSettings.value("userFeature/User3Key", "")))
                    
            if self.User4_vocTotal != 0:
                self.User4_number_voc.setText(str(self.User4_vocTotal))
                self.User4_horizontalLayout.show()                
                if appSettings.value("userFeature/User4Key", "")  !="":
                    self.User4_reminderLabel.setText(str(appSettings.value("userFeature/User4Key", "")))
                    
            if self.User5_vocTotal != 0:
                self.User5_number_voc.setText(str(self.User5_vocTotal))
                self.User5_horizontalLayout.show()                
                if appSettings.value("userFeature/User5Key", "")  !="":
                    self.User5_reminderLabel.setText(str(appSettings.value("userFeature/User5Key", "")))
                

        
        self.connect(self.start_voc2brain, QtCore.SIGNAL('clicked()'), self.start_vtb)
        print "### Show Window ... ###"
        self.show()
        


    def dont_remember_anymore(self):
        #Get path for config file
        #check os
        if operating_system == 'linux2' or operating_system == 'darwin':
                config_dir = backup_dirs = os.path.abspath(os.path.expanduser(u'~')+u'/.voc2brain/config.txt')
                
        elif operating_system == 'win32':
                config_dir = os.path.join(os.environ[u'APPDATA'], u'voc2brain/config.txt')
                                    
        else:
                config_dir = os.path.join(os.path.abspath(u'.'),u'config.txt')
                
        if self.dont_remember.checkState() == 2:
            appSettings.setValue("mainConfig/reminderKey", "no")


        elif self.dont_remember.checkState() == 0:    
            appSettings.setValue("mainConfig/reminderKey", "yes")
                
        def closeEvent(self, event):
            app.quit()
        
erinnern = appSettings.value("mainConfig/reminderKey","yes")
notifikations = appSettings.value("mainConfig/NotificationReminderKey","yes")
w_notify = appSettings.value("mainConfig/WindowReminderKey","no")

mainReminder = TriggerReminderClass()
sys.exit(app.exec_())





