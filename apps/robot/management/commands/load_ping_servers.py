# -*- encoding: utf-8 -*-
import logging

from apps.robot.models import PingServer
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = 'file_name'
    help = 'sending ping to search server'

    def handle(self, *args, **options):
        try:
            f = open(args[0], 'r')
            lines = f.readlines()
            i = 0
            j = 0
            for line in lines:
                i = i + 1
                line = line.replace('\n', '').replace('\r', '')
                _ping = PingServer.objects.all().filter(address=line)
                if _ping.count()==0:
                    ping = PingServer.objects.create(address=line)
                    ping.save()
                    j = j + 1
                    try:
                        logging.info('Adding server ' + line + ' - ok ' + str(j) + ' from ' + str (i))
                    except:
                        logging.exception('Error adding server ' + line)
            logging.info('loaded ' + str(j) + ' from ' + str (i))
        except:
            logging.exception('Error load ping servers')

