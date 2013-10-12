import site
site.addsitedir('/home/web/.envs/files/lib/python2.7/site-packages')
import os
import sys


path = '/home/web/files.doebi.at'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'files.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


import files.monitor
files.monitor.start(interval=1.0)
