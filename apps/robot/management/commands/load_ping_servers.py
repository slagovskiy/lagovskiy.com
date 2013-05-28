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
            for line in lines:
                _ping = PingServer.objects.all().filter(address=line)
                if _ping.count()==0:
                    ping = PingServer.objects.create(address=line.replace('\n', ''))
                    ping.save()
                    try:
                        logging.info('Adding server ' + line + ' - ok')
                    except:
                        logging.exception('Error adding server ' + line)
        except:
            logging.exception('Error load ping servers')

