from django.contrib.auth.models import AnonymousUser
from django.db.models import Count
import user_agents

from apps.statistic.models import *
from apps.statistic.utils import *
from apps.statistic.settings import *

import logging
from datetime import timedelta

class StatisticMiddleware:

    def process_request(self, request):
        if request.is_ajax(): return

        point = request.path
        user = request.user

        if isinstance(user, AnonymousUser):
            user = None

        agent = request.META.get('HTTP_USER_AGENT', '')
        ua = user_agents.parse(agent)
        ip = get_ip(request)
        session_key = request.session.session_key
        referer = request.META.get('HTTP_REFERER')

        if Visitor.objects.filter(
                date__range=(datetime.today()-timedelta(seconds=LIMIT_DUBLICATE_VISITORS), datetime.today()),
                point=point,
                user_agent=agent,
                ip_address=ip
        ).aggregate(Count('id'))['id__count'] == 0:
            v = Visitor.objects.create(
                point = point,
                user = user,
                user_agent = agent,
                session_key = session_key,
                ip_address = ip,
                referer = referer,
                browser_family = ua.browser.family,
                browser_version = ua.browser.version_string,
                os_family = ua.os.family,
                os_version = ua.os.version_string,
                device_family = ua.device.family,
                is_mobile = ua.is_mobile,
                is_tablet = ua.is_tablet,
                is_touch_capable = ua.is_touch_capable,
                is_pc = ua.is_pc,
                is_bot = ua.is_bot
            )
            v.save()
        else:
            logging.warning('Too many visitors from on point')

    def process_response(self, request, response):
        return response

