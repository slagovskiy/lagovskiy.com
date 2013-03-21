from django.contrib.auth.models import AnonymousUser
from django.db.models import Count

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
                referer = referer
            )
            v.save()
        else:
            logging.warning('Too many visitors from on point')

    def process_response(self, request, response):
        return response

