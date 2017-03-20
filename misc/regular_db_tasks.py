from PyQt5 import uic, QtWidgets
import time
from database.database_table_definitions import Vocabulary_Table, Deleted_Vocabulary_Table, Config_Table, Metadata_Table,  Activity_Table

# ABOUT DIALOG
class RegularDBTasksClass(object):
    def __init__(self, main_window):
        self.main_window = main_window

    def show_delete_dialog(self, list_of_cards):
        """
        Receives a list with card_ids and asks the user if he really wants to delete them.
        If the user agrees to delete them the delete_cards function will run.

        """
        ask_message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, self.main_window.tr("Delete words"),
                                            self.main_window.tr(
                                                "Do you really want to delete the selected cards? Amount of cards selected:" + " " + str(len(list_of_cards))))
        ask_message.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        ret = ask_message.exec_()

        if ret == QtWidgets.QMessageBox.Yes:
            self.delete_cards(list_of_cards)
        else:
            pass

    def delete_cards(self, list_of_cards):
        """

        Delete cards from "Vocabulary_Table" and add them to the "Deleted_Vocabulary_Table

        """
        for card_id in list_of_cards:
            card = self.main_window.session.query(Vocabulary_Table).filter(
                Vocabulary_Table.card_id == card_id).first()

            self.main_window.session.delete(card)

            self.main_window.session.add(
                Deleted_Vocabulary_Table(delete_date=time.time(), front=card.front, back=card.back))
            self.main_window.session.commit()

            # Update QTableView by emitting the "editing_finished_signal"
            self.main_window.communicate.editing_finished_signal.emit()