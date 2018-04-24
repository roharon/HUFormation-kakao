import os
import sys
 
path = '/home/roharon98/huformation_assistant/'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'hufscoops_project.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()