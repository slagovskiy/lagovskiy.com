from django.contrib.auth.models import AnonymousUser
from django.db.models import Count
import user_agents

from .models import Visitor
from ..toolbox.network import get_ip
from .settings import DUBLICATE_TIME_LIMIT

import logging
from datetime import timedelta, datetime


class StatisticMiddleware:

    def process_request(self, request):
        if request.is_ajax():
            return

        point = request.path
        agent = request.META.get('HTTP_USER_AGENT', '')
        ua = user_agents.parse(agent)
        ip = get_ip(request)
        session_key = request.session.session_key
        referer = request.META.get('HTTP_REFERER')

        if Visitor.objects.filter(
                date__range=(datetime.today()-timedelta(seconds=DUBLICATE_TIME_LIMIT), datetime.today()),
                point=point,
                user_agent=agent,
                ip_address=ip
        ).aggregate(Count('id'))['id__count'] == 0:
            v = Visitor.objects.create(
                point=point,
                user_agent=agent,
                session_key=session_key,
                ip_address=ip,
                referer=referer,
                browser_family=ua.browser.family,
                browser_version=ua.browser.version_string,
                os_family=ua.os.family,
                os_version=ua.os.version_string,
                device_family=ua.device.family,
                is_mobile=ua.is_mobile,
                is_tablet=ua.is_tablet,
                is_touch_capable=ua.is_touch_capable,
                is_pc=ua.is_pc,
                is_bot=ua.is_bot
            )
            v.save()
        else:
            logging.warning('Too many visitors from on point')

    def process_response(self, request, response):
        return response
