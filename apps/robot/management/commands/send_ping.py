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

from django.core.mail import EmailMultiAlternatives
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.mail import send_mail

class Command(NoArgsCommand):
    help = 'sending ping to search server'

    def handle_noargs(self, **options):
        report = []
        for p in Post.objects.all().filter(do_ping=True):
            logging.info('Page: ' + DOMAIN_NAME + p.get_absolute_url())
            for s in PingServer.objects.all().filter(deleted=False):
                try:
                    rpc = xmlrpclib.Server(s.address)
                    r = rpc.weblogUpdates.ping(DOMAIN_NAME, DOMAIN_NAME + p.get_absolute_url())
                    pr = PingResult.objects.create(
                        passed = not r['flerror'],
                        message = r['message'],
                        post = p,
                        pingserver = s
                    )
                    pr.save()
                    report.append([pr.date, pr.passed, pr.pingserver, pr.message])
                    logging.info(s.address + ' (page) ' + str(pr.date) + ' ' + str(pr.passed))
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
                    logging.warn(s.address + ' (page) ' + str(pr.date) + ' ' + pr.message)
                    #logging.exception('Error send ping')
            p.do_ping = False
            p.save()
        if len(report)>0:
            for adm in ADMINS:
                try:
                    c = Context(
                            {
                            'page_title': 'Ping report',
                            'report': report,
                            }
                    )
                    subject = u'Ping report [' + DOMAIN_NAME + ']'
                    from_email = EMAIL_SUBJECT_PREFIX + ' <' + DEFAULT_FROM_EMAIL + '>'
                    to = adm[1]
                    text_content = loader.get_template('robot/email_ping_text.html').render(c)
                    html_content = loader.get_template('robot/email_ping_html.html').render(c)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                except:
                    logging.exception('Error send ping report')