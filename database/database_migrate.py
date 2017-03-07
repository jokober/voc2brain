# -*- coding: utf-8 -*-
from database_table_definitions import Vocabulary_Table, Deleted_Vocabulary_Table, Config_Table, Metadata_Table, Activity_Table
from sqlalchemy import Table
import datetime

# Manage and show the items in TableView Widget
class DatabaseMigrateClass(object):
    def __init__(self, main_window):
        self.main_window = main_window

    def check_version(self):
        version = self.main_window.session.query(Vocabulary_Table).first()
        print "### Version #### " + unicode(version)

        if version == None:
            self.upgrade_to_vers1()

    def upgrade_to_vers1(self):
        print "### Info ### Migrate to database version 1"

        try:
            # Migrate old "vocabulary" table to "vocabulary_table"
            old_vocabulary_table = Table('vocabulary', self.main_window.base.metadata, autoload=True, autoload_with=self.main_window.local_engine)

        except:
            return

        for row in self.main_window.session.query(old_vocabulary_table).all():

            #
            if row.date == "random":
                new_date = None
            else:
                date_string = row.date.split("-")
                new_date = datetime.date(int(date_string[0]),int(date_string[1]), int(date_string[2]))
                print new_date
            # Set the createdDate to a random date in the past
            createdDate = datetime.date(1,1,1)

            print 'hier'
            print type(new_date)
            print new_date
            self.main_window.session.add(Vocabulary_Table(front = row.front, back = row.back, date_next_practice = new_date, deck = row.phase, createdDate = createdDate, course_name = row.language, lesson_name = "1"))
        self.main_window.session.commit()

        # Delete old "vocabulary" table
        old_vocabulary_table.drop(self.main_window.local_engine)

        # Add database Version number
        self.main_window.session.add(Metadata_Table(key = "db_version", value="1"))
        self.main_window.session.commit()