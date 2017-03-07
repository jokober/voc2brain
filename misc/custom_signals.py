from PyQt5 import QtCore

# CLASS WHICH MANAGES CUSTOM SIGNALS
class Communicate(QtCore.QObject):
    # Mixed signals
    new_update_available_signal = QtCore.pyqtSignal()
    editing_finished_signal = QtCore.pyqtSignal()
    update_graphs_signal = QtCore.pyqtSignal()
    new_practice_card_signal = QtCore.pyqtSignal()

    # Signals in RightorWrong dialog
    right_answer_signal = QtCore.pyqtSignal(int)
    wrong_answer_signal = QtCore.pyqtSignal(int)
    close_dialog_signal = QtCore.pyqtSignal()
    right_answer_inexamMode_signal = QtCore.pyqtSignal()
    wrong_answer_inexamMode_signal = QtCore.pyqtSignal()
    close_dialog_inexamMode_signal = QtCore.pyqtSignal()