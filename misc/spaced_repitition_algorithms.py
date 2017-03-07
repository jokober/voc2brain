# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import and_
from random import randrange
from database.database_table_definitions import Vocabulary_Table, Deleted_Vocabulary_Table, Config_Table, Metadata_Table, Activity_Table
from tabs.configuration_tab import ConfigDictClass

class LeitnerSystemClass(object):
    def __init__(self, main_window):
        self.main_window = main_window

        self.config_dict = ConfigDictClass(self.main_window).get_config_dict()

    # RETURNS "new_date_next_practice" BASED ON THE CURRENT DECK AND THE CORRESPONDING SETTINGS
    def get_date_next_practice(self, current_card_object, new_deck):
        list_of_decks_and_keystrings = [
            (1, "mainConfig/phase1"),
            (2, "mainConfig/phase2"),
            (3, "mainConfig/phase3"),
            (4, "mainConfig/phase4"),
            (5, "mainConfig/phase5"),
            (6, "mainConfig/phase6")
        ]

        for deck, key_string in list_of_decks_and_keystrings:
            if new_deck == deck:
                new_date_next_practice = datetime.date.today()+datetime.timedelta(int(self.config_dict[key_string]))
            else:
                print "### Warning ### No corresponding deck found for:" + str(new_deck)


        return new_date_next_practice #returns datetime

