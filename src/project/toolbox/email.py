from threading import Thread
from flask.ext.mail import Message
from flask import render_template
from config import ADMINS, MAIL_USERNAME, SITE_NAME
from project import app, mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()


def admin_notification(subject, message):
    send_email(
            subject,
            MAIL_USERNAME,
            ADMINS,
            render_template('email/admin_notification.txt', message=message),
            render_template('email/admin_notification.html', message=message)
    )


def send_email_registration(user):
    send_email(
        '[' + SITE_NAME + '] Registration',
        MAIL_USERNAME,
        [user.email],
        render_template('email/register_notification.txt', user=user, site=SITE_NAME),
        render_template('email/register_notification.html', user=user, site=SITE_NAME)
    )
    admin_notification('[' + SITE_NAME + '] New user', 'Registered new user [' + user.username + ']')
