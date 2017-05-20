from PyQt5 import QtCore

# CLASS WHICH MANAGES CUSTOM SIGNALS
class Communicate(QtCore.QObject):
    # Mixed signals
    new_update_available_signal = QtCore.pyqtSignal()
    editing_finished_signal = QtCore.pyqtSignal()
    new_practice_card_signal = QtCore.pyqtSignal()

    # Signals for configurations
    config_updated = QtCore.pyqtSignal()

    # Signals in RightorWrong dialog
    right_answer_signal = QtCore.pyqtSignal(int)
    wrong_answer_signal = QtCore.pyqtSignal(int)