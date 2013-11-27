import os
import sys

''' Apache conf

# ==================[domain.tld]==================== 
<VirtualHost *:80>
    ServerName domain.tld
    ServerAlias www.domain.tld
    ServerAdmin slagovskiy@gmail.com
    DocumentRoot /home/domain.tld
    ErrorLog /home/domain.tld/logs/error.log
    CustomLog /home/domain.tld/logs/access.log combined

    WSGIScriptAlias / /home/domain.tld/django.wsgi

    #Alias /robots.txt /home/domain.tld/robots.txt
    #Alias /favicon.ico /home/domain.tld/favicon.ico
    Alias /media /home/domain.tld/media
    Alias /static /home/domain.tld/static
</VirtualHost>
# ==================[domain.tld]==================== 

'''

sys.path.append('/var/www/Odyssey')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

path = os.path.dirname(os.path.realpath(__file__))
if path not in sys.path:
   sys.path.append(path)