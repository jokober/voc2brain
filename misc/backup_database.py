# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtWidgets
from shutil import copyfile
import datetime
import os

from os_adjustments import os_adjustment_object

from database.database_table_definitions import Config_Table

class BackupDatabaseClass(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.backup_path =  self.main_window.session.query(Config_Table).filter_by(key="mainConfig/backup_path").first().value
        self.database_path = os_adjustment_object.database_path

        # Open "backupPage"
        self.main_window.configTabs.setCurrentIndex(3)

        # Starts the backup process
        self.list_all_backups()
        self.show_recent_backups_in_tableView()

        self.main_window.save_backup_button.clicked.connect(lambda: self.backup_database())
        self.main_window.select_backup_folder_button.clicked.connect(self.select_backup_folder)
        self.main_window.use_default_dir_button.clicked.connect(self.reset_backup_folder)

    # GET A LIST OF ALL FILES IN THE BACKUP DIREKTORY
    def list_all_backups(self):
        files_in_directory = []
        for (dirpath, dirnames, filenames) in os.walk(str(self.backup_path)):
            files_in_directory.extend(filenames)

        self.date_list = []
        for filename in files_in_directory:
            if len(filename) == 27:
                try:
                    prefix = filename[:17]
                    date_string = filename[-10:]
                except:
                    print "### Info ### File not recognised"

                if  prefix == "voc2brain_backup_":
                    date_string = date_string.split('-')
                    file_date = datetime.date(int(date_string[0]), int(date_string[1]),int(date_string[2]))
                    self.date_list.append(file_date)

        # Sort list by date
        self.date_list.sort(reverse=True)
        print datetime.date.today()
        print self.date_list[0]
        print datetime.date.today()-self.date_list[0]


        # Checks if a new backup is required
        if len(self.date_list) == 0:
            self.backup_database()

        elif datetime.date.today()-self.date_list[0] > datetime.timedelta(10):
            print 'pups'
            self.backup_database()

        # Checks if old backups are redundant (20 backups are maximum) - if yes: runf function to deletes them
        if len(self.date_list)>20:
            self.delete_old_backup()

        self.show_recent_backups_in_tableView()

    # A COPY OF THE DATABASE FILE WILL BE SAVED IN FOLLOWING FORMAT: "voc2brain_backup_DDMMYYYY.sdb3"
    def backup_database(self):
        print "### Info ### Save a new Backup"
        copyfile(self.database_path, os.path.abspath(self.backup_path + U'/voc2brain_backup_' + str(datetime.date.today())))
        self.list_all_backups()

    # DELETE THE OLDEST BACKUP FILES
    def delete_old_backup(self):
        print "### Info ### Delete redundant backups"
        for i in range(len(self.date_list)-20):
            os.remove(os.path.abspath(self.backup_path + U'/voc2brain_backup_' + str(self.date_list[0])+ ".sdb3") )

    # SHOWS THE RECENT BACKUPS AND INITIATES THE BACKUP BY RUNNING THE
    def show_recent_backups_in_tableView(self):
        # standard item model
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels([self.main_window.tr('Filename'), self.main_window.tr('Date')])

        # Fill standard item model with data
        item = QtGui.QStandardItem
        print self.date_list
        for row in range(0, len(self.date_list)):
            model.setItem(row, 0, item("voc2brain_backup_"+str(self.date_list[row])+ ".sdb3"))
            model.setItem(row, 1, item(str(self.date_list[row])))

        # Connect tableview widget with filter_proxy_model
        self.main_window.recent_backup_tableView.setModel(model)
        self.main_window.recent_backup_tableView.setColumnWidth(0, 400)

    # OPENS A QFILEDIALOG AND ASKS FOR THE A NEW BACKUP FOLDER
    def select_backup_folder(self):
        load_dir = unicode(QtWidgets.QFileDialog.getExistingDirectory(self, self.main_window.tr('Select backup directory'), self.backup_path))

    # RESETS THE BACKUP FOLDER TO THE DEFAULT PATH
    def reset_backup_folder(self):
        pass
