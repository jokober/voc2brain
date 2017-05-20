from database.database_table_definitions import Vocabulary_Table, Deleted_Vocabulary_Table, Config_Table, Metadata_Table, Activity_Table
import datetime
from PyQt5 import QtCore, QtGui, uic, QtWidgets

class StatsTabClass(object):
    def __init__(self, main_window):
        self.main_window = main_window

        self.load_statistics_labels()

    def updateGraph(self, argList):
        return

    # LOADS THE VALUES FOR THE STATISTICS LABELS
    def load_statistics_labels(self):
        self.main_window.total_amount_of_cards.setText(unicode(self.main_window.session.query(Vocabulary_Table.card_id).count()))

        # Get amount of cards in each decks
        list_of_decks_and_ui_elements = [
            (1, self.main_window.statistics_label_deck1),
            (2, self.main_window.statistics_label_deck2),
            (3, self.main_window.statistics_label_deck3),
            (4, self.main_window.statistics_label_deck4),
            (5, self.main_window.statistics_label_deck5),
            (6, self.main_window.statistics_label_deck6),
            (7, self.main_window.statistics_label_deck7)
        ]

        for deck, ui_element in list_of_decks_and_ui_elements:
            ui_element.setText(unicode(self.main_window.session.query(Vocabulary_Table.card_id).filter(
                Vocabulary_Table.deck == deck).count()))

            list_of_ui_elements = [
                (self.main_window.today_label, self.main_window.aday),
                (self.main_window.today_plus1_label, self.main_window.aday),
                (self.main_window.today_plus2_label, self.main_window.bday),
                (self.main_window.today_plus3_label, self.main_window.cday),
                (self.main_window.today_plus4_label, self.main_window.dday),
                (self.main_window.today_plus5_label, self.main_window.eday),
                (self.main_window.today_plus6_label, self.main_window.fday)
            ]

            counter = 0
            for card_amount_element, day_element in list_of_ui_elements:
                date = datetime.date.today() + datetime.timedelta(counter)

                # leads the amount of cards to learn for each day
                card_amount_element.setText(unicode(self.main_window.session.query(Vocabulary_Table.card_id).filter(
                    Vocabulary_Table.date_next_practice == date ).count()))

                # loads the name of the weekday
                day_element.setText(self.find_Day(date.weekday()))

                counter = counter +1

    # Returns the weekday as string
    def find_Day(self, DayNumber):
        DayNumber = int(DayNumber)
        if DayNumber == 0:
            Daystring = self.main_window.tr("Sunday:")
        elif DayNumber == 1:
            Daystring = self.main_window.tr("Monday:")
        elif DayNumber == 2:
            Daystring = self.main_window.tr("Tuesday:")
        elif DayNumber == 3:
            Daystring = self.main_window.tr("Wednesday:")
        elif DayNumber == 4:
            Daystring = self.main_window.tr("Thursday:")
        elif DayNumber == 5:
            Daystring = self.main_window.tr("Friday:")
        elif DayNumber == 6:
            Daystring = self.main_window.tr("Saturday:")

        return Daystring