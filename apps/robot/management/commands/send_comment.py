# -*- encoding: utf-8 -*-
import logging
import re
from django.core.management.base import NoArgsCommand
from django.core.management.base import BaseCommand, CommandError
from time import sleep
from django.template import loader, Context

import xmlrpclib
import sys

from apps.blog.models import Post, CommentMessageQueue, Comment
from apps.robot.models import *
from apps.robot.settings import *
from settings import *

import smtplib
from django.core.mail import EmailMultiAlternatives
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.mail import send_mail

class Command(NoArgsCommand):
    help = 'sending comments to subscribers'

    def handle_noargs(self, **options):
        comment_queue = CommentMessageQueue.objects.all().filter(active=True)
        logging.warning(comment_queue)
        for task in comment_queue:
            try:
                if task.subscribe.active:
                    c = Context(
                            {
                            'task': task
                            }
                    )

                    subject = u'New comment [' + task.comment.post.title + ']'
                    from_email = EMAIL_SUBJECT_PREFIX + ' <' + DEFAULT_FROM_EMAIL + '>'
                    to = task.subscribe.email
                    text_content = loader.get_template('robot/email_comment_text.html').render(c)
                    html_content = loader.get_template('robot/email_comment_html.html').render(c)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
            except:
                logging.exception('Error send comment notification')
            #task.active = False
            #task.save()