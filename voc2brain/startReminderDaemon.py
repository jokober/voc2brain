#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,time,sys
import voc2brain
import daemon
import lockfile
from PyQt5 import QtWidgets
from daemon import pidfile

def checkNow(mainWindow):
    while True:
        toLearnToday = mainWindow.checkVocs2learn()
        if toLearnToday > -1:
            os.system("notify-send 'Vocabularies to learn today:' " + str(toLearnToday))
        time.sleep(10)


if __name__ == "__main__":
    voc2brain_app = QtWidgets.QApplication(sys.argv)
    voc2brain_app.setOrganizationName("Voc2brain")
    voc2brain_app.setOrganizationDomain("voc2brain.sf.net")
    voc2brain_app.setApplicationName("voc2brain")
    voc2brain_app.setAttribute(10)

    mainWindow = voc2brain.MainWindow(voc2brain_app)

    with daemon.DaemonContext(pidfile=pidfile.TimeoutPIDLockFile('/tmp/foo.pid',5)):
        checkNow(mainWindow)
