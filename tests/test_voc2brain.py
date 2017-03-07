# -*- coding: utf-8 -*-

import sys
import unittest
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt


def test_defaults(self):
    '''Test the GUI in its default state'''
    self.assertEqual(self.form.ui.tequilaScrollBar.value(), 8)
    self.assertEqual(self.form.ui.tripleSecSpinBox.value(), 4)
    self.assertEqual(self.form.ui.limeJuiceLineEdit.text(), "12.0")
    self.assertEqual(self.form.ui.iceHorizontalSlider.value(), 12)
    self.assertEqual(self.form.ui.speedButtonGroup.checkedButton().text(), "&Karate Chop")

    # Class is in the default state even without pressing OK
    self.assertEqual(self.form.jiggers, 36.0)
    self.assertEqual(self.form.speedName, "&Karate Chop")

    # Push OK with the left mouse button
    okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
    QTest.mouseClick(okWidget, Qt.LeftButton)
    self.assertEqual(self.form.jiggers, 36.0)
    self.assertEqual(self.form.speedName, "&Karate Chop")