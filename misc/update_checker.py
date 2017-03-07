import sys
import urllib2
#from voc2brain import Communicate

# CHECKS IF THERE IS A NEW VERSION OF Voc2brain AVAILABLE
class search_for_update_class(object):
    def __init__(self, communicate):
        operating_system = unicode(sys.platform)
        self.communicate = communicate

    def __run__(self):
        if operating_system != 'linux2':

            try:
                response=urllib2.urlopen('http://www.google.com',timeout=3)

                f = urllib.urlopen("http://voc2brain.sourceforge.net/voc2brain_version.txt")
                for zeile in f:
                    zeile = zeile.split(" ")

                    if operating_system == 'win32':
                        OS = "Windows"
                    elif operating_system == 'darwin':
                        OS = "Windows"

                    print zeile[0], OS
                    if zeile[0] == OS:
                        newUpdate = False
                        new_version = zeile[1].split('.')

                        version = (4,00,00)

                        print version[0]

                        print new_version[0]

                        if new_version[0] < version[0]:
                            newUpdate = False
                        elif new_version[0] > version[0]:
                            newUpdate = True
                        elif new_version[0] == version[0]:
                            print 1
                            if new_version[1] <= version[1]:
                                newUpdate = False
                            elif new_version[1] >= version[1]:
                                newUpdate = True
                            elif new_version[1] == version[1]:
                                print 2
                                if new_version[2] <= version[2]:
                                    newUpdate = False
                                elif new_version[2] >= version[2]:
                                    newUpdate = True
                                    print "[No update available]"
                                else:
                                    newUpdate = False
                                    print "[Update available]"
                        print newUpdate

                if newUpdate:
                    self.communicate.new_update_available_signal.emit()

                f.close()

            except urllib2.URLError:
                print "No internet connection ..."

