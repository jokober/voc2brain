

import os, sys

# CLASS WHICH MANAGES ADJUSTMENTS FOR THE SPECIFIC OS
class os_adjustment_object(object):
    def __init__(self, main_window):
        self.operating_system = unicode(sys.platform)

        if self.operating_system == 'linux2':
            if main_window.development_version == True:
                self.workplace = os.path.abspath(os.path.expanduser(u'~') + u'/.voc2brain/development')
            elif main_window.development_version == False:
                self.workplace = os.path.abspath(os.path.expanduser(u'~') + u'/.voc2brain')
            else:
                print " #### Error: ### No version found (development version)"

            self.database_path = os.path.abspath(self.workplace + u'/vocabulary.sdb3')
            self.backup_dirs = os.path.abspath(self.workplace + u'/backups')

            self.stylesheet_plastique = [os.path.join(os.path.abspath(u'.'), u'stylesheets/plastique.qss'),
                                    os.path.join(os.path.abspath(u'.'), u'stylesheets/plastique_background.qss')]
            self.stylesheet_green = [os.path.join(os.path.abspath(u'.'), u'stylesheets/green.qss'),
                                os.path.join(os.path.abspath(u'.'), u'stylesheets/green_background.qss')]
            self.stylesheet_pink = [os.path.join(os.path.abspath(u'.'), u'stylesheets/pink.qss'),
                               os.path.join(os.path.abspath(u'.'), u'stylesheets/pink_background.qss')]
            self.stylesheet_general = [os.path.join(os.path.abspath(u'.'), u'stylesheets/general.qss'),
                                  os.path.join(os.path.abspath(u'.'), u'stylesheets/general_background.qss')]

            if not os.path.exists(os.path.abspath(os.path.expanduser(u'~') + u'/.voc2brain')):
                os.mkdir(os.path.abspath(os.path.abspath(os.path.expanduser(u'~') + u'/.voc2brain')))

            if not os.path.exists(self.workplace):
                os.mkdir(self.workplace)

            if not os.path.exists(os.path.abspath(self.workplace + u'/backups')):
                os.mkdir(os.path.abspath(self.workplace + u'/backups'))

        elif self.operating_system == "darwin":
            self.workplace = os.path.abspath(os.path.expanduser(u'~') + u'/Library/Application Support/voc2brain')
            self.database_path = os.path.abspath(workplace + u'/vocabulary.sdb3')
            self.backup_dirs = os.path.abspath(workplace + u'/backups')

            self.stylesheet_plastique = [os.path.join(os.path.abspath(u'.'), u'stylesheets/plastique.qss'),
                                    os.path.join(os.path.abspath(u'.'), u'stylesheets/plastique_background.qss')]
            self.stylesheet_green = [os.path.join(os.path.abspath(u'.'), u'stylesheets/green.qss'),
                                os.path.join(os.path.abspath(u'.'), u'stylesheets/green_background.qss')]
            self.stylesheet_pink = [os.path.join(os.path.abspath(u'.'), u'stylesheets/pink.qss'),
                               os.path.join(os.path.abspath(u'.'), u'stylesheets/pink_background.qss')]
            self.stylesheet_general = [os.path.join(os.path.abspath(u'.'), u'stylesheets/general.qss'),
                                  os.path.join(os.path.abspath(u'.'), u'stylesheets/general_background.qss')]

            if not os.path.exists(self.workplace):
                os.mkdir(os.path.abspath(self.workplace))

            if not os.path.exists(self.backup_dirs):
                os.mkdir(os.path.abspath(self.backup_dirs))



        elif self.operating_system == 'win32':
            self.workplace = os.path.join(os.environ[u'APPDATA'], os.path.normcase(u"voc2brain"))
            self.database_path = os.path.join(os.environ[u'APPDATA'], os.path.normcase(u'voc2brain/vocabulary.sdb3'))
            self.statistics_database_path = os.path.join(os.environ[u'APPDATA'], os.path.normcase(u'voc2brain/UserStat.sdb3'))
            self.backup_dirs = os.path.join(os.environ[u'APPDATA'], os.path.normcase(u'voc2brain/backups'))

            self.stylesheet_plastique = [os.path.join(os.path.abspath(u'.'), u'stylesheets/plastique.qss'),
                                    os.path.join(os.path.abspath(u'.'), u'stylesheets/plastique_background.qss')]
            self.stylesheet_green = [os.path.join(os.path.abspath(u'.'), u'stylesheets/green.qss'),
                                os.path.join(os.path.abspath(u'.'), u'stylesheets/green_background.qss')]
            self.stylesheet_pink = [os.path.join(os.path.abspath(u'.'), u'stylesheets/pink.qss'),
                               os.path.join(os.path.abspath(u'.'), u'stylesheets/pink_background.qss')]
            self.stylesheet_general = [os.path.join(os.path.abspath(u'.'), u'stylesheets/general.qss'),
                                  os.path.join(os.path.abspath(u'.'), u'stylesheets/general_background.qss')]

            if not os.path.exists(os.path.join(os.environ[u'APPDATA'], os.path.normcase(u'voc2brain'))):
                os.mkdir(os.path.join(os.environ[u'APPDATA'], os.path.normcase(u'voc2brain')))

            if not os.path.exists(os.path.join(os.environ[u'APPDATA'], os.path.normcase(u'voc2brain/backups'))):
                os.mkdir(os.path.join(os.environ[u'APPDATA'], os.path.normcase(u'voc2brain/backups')))

            # sys.stderr = open(os.path.join(workplace, "v2b_log.txt"),"w")
