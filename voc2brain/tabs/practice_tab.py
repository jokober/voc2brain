# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore, uic, QtWidgets
import datetime, time
from sqlalchemy import and_
from random import randrange

from dialogs.rightorwrong_dialog import Right_or_Wrong_Class

from misc.spaced_repitition_algorithms import LeitnerSystemClass

from database.database_table_definitions import Vocabulary_Table, Deleted_Vocabulary_Table, Config_Table, Metadata_Table, Activity_Table

class PracticeTabClass(object):
    def __init__(self, main_window):
        self.main_window = main_window
        self.load_new_card()
        self.LeitnerSystem = LeitnerSystemClass(self.main_window)
        self.main_window.communicate.new_practice_card_signal.connect(self.load_new_card)

        self.main_window.communicate.right_answer_signal.connect(self.isright)
        self.main_window.communicate.wrong_answer_signal.connect(self.iswrong)
        self.main_window.check_answer_button.clicked.connect(lambda: self.check_answer())
        self.main_window.skip_button.clicked.connect(lambda: self.load_new_card())

    # MANAGES THE PRACTICE
    def load_new_card(self):
        self.main_window.flip_side_textedit.setPlainText(u'')

        # Go through all course_names and select the due cards in every course
        for course_string in self.main_window.session.query(Vocabulary_Table.course_name).distinct():
            cards_to_learn = self.main_window.session.query(Vocabulary_Table).filter(and_(
                Vocabulary_Table.course_name ==course_string.course_name,
                Vocabulary_Table.date_next_practice <= datetime.date.today()))
            print unicode(cards_to_learn)
            amount_due_cards = len(cards_to_learn.all())
            if amount_due_cards !=0:
                self.main_window.amount_due_cards_label.setText(unicode(amount_due_cards))
                single_card_to_learn = cards_to_learn[randrange(0, amount_due_cards)]

                self.main_window.front_side_textedit.setPlainText(unicode(single_card_to_learn.front))
                self.main_window.flip_side_textedit.setEnabled(True)
                self.main_window.flip_side_textedit.setFocus()
                self.main_window.deck_indicator_Bar.setValue(single_card_to_learn.deck)


                return # Return if a due card has been found

        # This will only run if no due cards have been found in the loop above
        self.main_window.deck_indicator_Bar.setValue(0)
        self.main_window.amount_due_cards_label.setText(unicode(0))
        self.main_window.flip_side_textedit.setPlainText(u'')
        self.main_window.front_side_textedit.setPlainText(u'')
        self.main_window.flip_side_textedit.setEnabled(False)

        if time.time() - self.main_window.seconds2 >= 6:
            informations = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, self.main_window.tr("Hooray!"), self.main_window.tr(
                "You have been sufficient studiously today - you looked through all available words"))
            informations.exec_()

    # CHECKS THE ANSWER AND DECIDES WHEATHER 'right_or_wrong" DIALOG SHOULD BE OPENED OR NOT
    def check_answer(self):
        print "Checking Answer"
        if unicode(self.main_window.flip_side_textedit.toPlainText()) == '':
            error = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, self.main_window.tr("Failing entry"), self.main_window.tr("You must give an answer!"))
            error.exec_()

        else:
            current_card = self.main_window.session.query(Vocabulary_Table).filter(Vocabulary_Table.front == self.main_window.front_side_textedit.toPlainText()).first()

            given_answer = unicode(self.main_window.flip_side_textedit.toPlainText())
            correct_answer = unicode(current_card.back)

            if correct_answer == unicode(given_answer):
                self.main_window.communicate.right_answer_signal.emit(correct_answer)
                self.main_window.flip_side_textedit.setPlainText('')

            else:
                self.right_or_wrong_dialog = Right_or_Wrong_Class(given_answer, current_card.card_id, self.main_window, "NormalMode")
                self.right_or_wrong_dialog.show()
                self.main_window.flip_side_textedit.setPlainText('')

    # UPDATE CORRECTLY ANSWERED CARD
    def isright(self, card_id):
        current_card_object = self.main_window.session.query(Vocabulary_Table).filter(Vocabulary_Table.card_id == card_id).first()
        old_deck = int(current_card_object.deck)
        if old_deck == 6:
            new_deck = 7
            new_date_next_practice = None
            congratulation = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                               unicode(self.main_window.tr("Congratulations!")), unicode(self.main_window.tr(
                    "Congratulations!!! - The vocabulary has reached the seventh level. It will probably stay in your long-term memory forever!")))
            congratulation.exec_()

            # insert "word_completed" activity into the Activity_Table
            self.main_window.session.add(Activity_Table(value="word_completed", card_id=card_id))

        else:
            new_deck = old_deck +1
            new_date_next_practice = self.LeitnerSystem.get_date_next_practice(current_card_object, new_deck)

        # insert "right" activity in the database
        self.main_window.session.add(Activity_Table(value="right", card_id=card_id))

        # update the card in the database
        self.main_window.session.query(Vocabulary_Table).filter_by(card_id=card_id).update({'deck': new_deck, "date_next_practice" : new_date_next_practice})

        # commit all changes to database
        self.main_window.session.commit()

        # load new card
        self.load_new_card()

    # UPDATE WRONGLY ANSWERED CARD
    def iswrong(self, card_id):
        current_card_object = self.main_window.session.query(Vocabulary_Table).filter(Vocabulary_Table.card_id == card_id).first()

        new_deck = 1
        new_date_next_practice = self.LeitnerSystem.get_date_next_practice(current_card_object, new_deck)

        # insert "wrong" activity in the database
        self.main_window.session.add(Activity_Table(value="wrong", card_id=card_id))

        # update the card in the database
        self.main_window.session.query(Vocabulary_Table).filter_by(card_id=card_id).update({'deck': new_deck, "date_next_practice" : new_date_next_practice})

        # commit all changes to database
        self.main_window.session.commit()

        # load new card
        self.load_new_card()


    # CLOSES THE "RIGHT_or_WRONG" DIALOG
    def close_rightorwrong(self):

        self.main_window.flip_side_textedit.activateWindow()
        self.main_window.askDialog.close()
        del self.main_window.askDialog

        self.main_window.new_question()
        self.main_window.flip_side_textedit.setFocus()

    def update_color_animation(self):
        self.frame = self.frame + 1

        if self.frame != 0 and self.frame <= 17:
            self.alpha = self.alpha + 15

        if self.frame != 0 and self.frame >= 17:
            self.alpha = self.alpha - 15

        self.frame_2.setStyleSheet("background-color: rgb(85, 255, 0,%s);" % (str(self.alpha)))
        self.frame_2.setLineWidth(1)

        if self.frame == 33:
            self.frame = 0
            self.timer.stop()

    def update_color_animation_red(self):
        self.frame = self.frame + 1

        if self.frame != 0 and self.frame <= 17:
            self.alpha = self.alpha + 15

        if self.frame != 0 and self.frame >= 17:
            self.alpha = self.alpha - 15

        self.frame_2.setStyleSheet("background-color: rgba(255, 0, 0,%s);" % (str(self.alpha)))

        if self.frame == 33:
            self.frame = 0
            self.timerRed.stop()

    def show_Animation(self):
        self.statistics.StatisticsQueue.put((None, "right"))

        # Starts the Color Animation
        if os_adjustment_object.operating_system == 'win32':
            self.timer.start(25)
        else:
            self.timer.start(20)

    def show_AnimationRed(self):
        self.statistics.StatisticsQueue.put((None, "wrong"))
        # Starts the Color Animation
        if os_adjustment_object.operating_system == 'win32':
            self.timerRed.start(25)
        else:
            self.timerRed.start(20)