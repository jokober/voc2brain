

import os, sys

# CLASS WHICH MANAGES ADJUSTMENTS FOR THE SPECIFIC OS
class os_adjustment_object(object):
    operating_system = unicode(sys.platform)

    if operating_system == 'linux2':
        workplace = os.path.abspath(os.path.expanduser(u'~') + u'/.voc2brain')
        database_path = os.path.abspath(os.path.expanduser(u'~') + u'/.voc2brain/vocabulary.sdb3')
        statistics_database_path = os.path.abspath(os.path.expanduser(u'~') + u'/.voc2brain/UserStat.sdb3')
        backup_dirs = os.path.abspath(os.path.expanduser(u'~') + u'/.voc2brain/backups')

        stylesheet_plastique = [os.path.join(os.path.abspath(u'.'), u'stylesheets/plastique.qss'),
                                os.path.join(os.path.abspath(u'.'), u'stylesheets/plastique_background.qss')]
        stylesheet_green = [os.path.join(os.path.abspath(u'.'), u'stylesheets/green.qss'),
                            os.path.join(os.path.abspath(u'.'), u'stylesheets/green_background.qss')]
        stylesheet_pink = [os.path.join(os.path.abspath(u'.'), u'stylesheets/pink.qss'),
                           os.path.join(os.path.abspath(u'.'), u'stylesheets/pink_background.qss')]
        stylesheet_general = [os.path.join(os.path.abspath(u'.'), u'stylesheets/general.qss'),
                              os.path.join(os.path.abspath(u'.'), u'stylesheets/general_background.qss')]

        if not os.path.exists(os.path.abspath(os.path.expanduser(u'~') + u'/.voc2brain')):
            os.mkdir(os.path.abspath(os.path.expanduser(u'~') + u'/.voc2brain'))

        if not os.path.exists(os.path.abspath(os.path.expanduser(u'~') + u'/.voc2brain/backups')):
            os.mkdir(os.path.abspath(os.path.expanduser(u'~') + u'/.voc2brain/backups'))

    elif operating_system == "darwin":
        workplace = os.path.abspath(os.path.expanduser(u'~') + u'/Library/Application Support/voc2brain')
        database_path = os.path.abspath(workplace + u'/vocabulary.sdb3')
        statistics_database_path = os.path.abspath(workplace + u'/UserStat.sdb3')
        backup_dirs = os.path.abspath(workplace + u'/backups')

        stylesheet_plastique = [os.path.join(os.path.abspath(u'.'), u'stylesheets/plastique.qss'),
                                os.path.join(os.path.abspath(u'.'), u'stylesheets/plastique_background.qss')]
        stylesheet_green = [os.path.join(os.path.abspath(u'.'), u'stylesheets/green.qss'),
                            os.path.join(os.path.abspath(u'.'), u'stylesheets/green_background.qss')]
        stylesheet_pink = [os.path.join(os.path.abspath(u'.'), u'stylesheets/pink.qss'),
                           os.path.join(os.path.abspath(u'.'), u'stylesheets/pink_background.qss')]
        stylesheet_general = [os.path.join(os.path.abspath(u'.'), u'stylesheets/general.qss'),
                              os.path.join(os.path.abspath(u'.'), u'stylesheets/general_background.qss')]

        if not os.path.exists(workplace):
            os.mkdir(os.path.abspath(workplace))

        if not os.path.exists(backup_dirs):
            os.mkdir(os.path.abspath(backup_dirs))



    elif operating_system == 'win32':
        workplace = os.path.join(os.environ[u'APPDATA'], os.path.normcase(u"voc2brain"))
        database_path = os.path.join(os.environ[u'APPDATA'], os.path.normcase(u'voc2brain/vocabulary.sdb3'))
        statistics_database_path = os.path.join(os.environ[u'APPDATA'], os.path.normcase(u'voc2brain/UserStat.sdb3'))
        backup_dirs = os.path.join(os.environ[u'APPDATA'], os.path.normcase(u'voc2brain/backups'))

        stylesheet_plastique = [os.path.join(os.path.abspath(u'.'), u'stylesheets/plastique.qss'),
                                os.path.join(os.path.abspath(u'.'), u'stylesheets/plastique_background.qss')]
        stylesheet_green = [os.path.join(os.path.abspath(u'.'), u'stylesheets/green.qss'),
                            os.path.join(os.path.abspath(u'.'), u'stylesheets/green_background.qss')]
        stylesheet_pink = [os.path.join(os.path.abspath(u'.'), u'stylesheets/pink.qss'),
                           os.path.join(os.path.abspath(u'.'), u'stylesheets/pink_background.qss')]
        stylesheet_general = [os.path.join(os.path.abspath(u'.'), u'stylesheets/general.qss'),
                              os.path.join(os.path.abspath(u'.'), u'stylesheets/general_background.qss')]

        if not os.path.exists(os.path.join(os.environ[u'APPDATA'], os.path.normcase(u'voc2brain'))):
            os.mkdir(os.path.join(os.environ[u'APPDATA'], os.path.normcase(u'voc2brain')))

        if not os.path.exists(os.path.join(os.environ[u'APPDATA'], os.path.normcase(u'voc2brain/backups'))):
            os.mkdir(os.path.join(os.environ[u'APPDATA'], os.path.normcase(u'voc2brain/backups')))

        # sys.stderr = open(os.path.join(workplace, "v2b_log.txt"),"w")