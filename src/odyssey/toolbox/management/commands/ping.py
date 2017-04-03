import logging
from django.core.management.base import BaseCommand

import xmlrpc.client
import sys

from ....blog.models import Post
from ...models import *
from ....settings import SITE_URL

from django.core.mail import EmailMultiAlternatives
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'sending ping to search server'

    def handle(self, **options):
        report = []
        for p in Post.objects.all().filter(do_ping=True, status = Post.PUBLISHED_STATUS):
            logging.info('Page: ' + p.get_post_url())
            for s in PingServer.objects.all().filter(deleted=False):
                try:
                    rpc = xmlrpc.client.(s.address)
                    r = rpc.weblogUpdates.ping(SITE_URL, p.get_post_url())
                    pr = PingResult.objects.create(
                        passed=not r['flerror'],
                        message=r['message'],
                        post=p,
                        pingserver = s
                    )
                    pr.save()
                    report.append([pr.date, pr.passed, pr.pingserver, pr.message])
                    logging.info(s.address + ' (page) ' + str(pr.date) + ' ' + str(pr.passed))
                except Exception as err:
                    pr = PingResult.objects.create(
                        passed=False
                    )
                    try:
                        pr.message = str(sys.exc_info()[0]).replace('<', '').replace('>', '')
                    except:
                        pr.message = ''
                    pr.post = p
                    pr.pingserver = s
                    pr.save()
                    report.append([pr.date, pr.passed, pr.pingserver, pr.message])
            p.do_ping = False
            p.save()
'''
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
'''