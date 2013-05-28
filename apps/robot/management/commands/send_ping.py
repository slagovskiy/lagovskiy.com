# -*- encoding: utf-8 -*-
import logging
import re
from django.core.management.base import NoArgsCommand
from django.core.management.base import BaseCommand, CommandError
from time import sleep
from django.template import loader, Context

import xmlrpclib
import sys

from apps.blog.models import Post
from apps.robot.models import *
from apps.robot.settings import *
from settings import *

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Command(NoArgsCommand):
    help = 'sending ping to search server'

    def handle_noargs(self, **options):
        report = []
        for p in Post.objects.all().filter(do_ping=True):
            for s in PingServer.objects.all().filter(deleted=False):
                logging.info(DOMAIN_NAME + p.get_absolute_url())
                try:
                    rpc = xmlrpclib.Server(s.address)
                    r = rpc.weblogUpdates.ping(p.title, DOMAIN_NAME + p.get_absolute_url())
                    pr = PingResult.objects.create(
                        passed = not r['flerror'],
                        message = r['message'],
                        post = p,
                        pingserver = s
                    )
                    pr.save()
                    report.append([pr.date, pr.passed, pr.pingserver, pr.message])
                    logging.info([pr.date, pr.passed, pr.pingserver, pr.message])
                except Exception, err:
                    pr = PingResult.objects.create(
                        passed = False
                    )
                    try:
                        pr.message = str(sys.exc_info()[0]).replace('<','').replace('>','')
                    except:
                        pr.message = ''
                    pr.post = p
                    pr.pingserver = s
                    pr.save()
                    report.append([pr.date, pr.passed, pr.pingserver, pr.message])
                    logging.exception('Error send ping')
        if len(report)>0:
            for adm in ADMINS:
                try:
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = u'[' + DOMAIN_NAME + '] Ping report'
                    msg['From'] = ROBOT_EMAIL
                    msg['To'] = adm[1]

                    c = Context(
                            {
                            'page_title': 'Ping report',
                            'report': report,
                            }
                    )

                    t = loader.get_template('robot/email_ping_text.html')
                    text = t.render(c)
                    t = loader.get_template('robot/email_ping_html.html')
                    html = t.render(c)

                    part1 = MIMEText(text, 'plain', 'utf-8')
                    part2 = MIMEText(html, 'html', 'utf-8')

                    msg.attach(part1)
                    msg.attach(part2)

                    s = smtplib.SMTP(ROBOT_SMTP)
                    s.login(ROBOT_LOGIN, ROBOT_PASSWORD)
                    s.sendmail(ROBOT_EMAIL, adm[1], msg.as_string())
                    s.quit()
                    logging.info('ping report sended')
                except:
                    logging.exception('Error send ping report')