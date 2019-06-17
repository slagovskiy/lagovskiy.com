from .models import Global


class GlobalsMiddleware:

    def process_request(self, request):
        g = {}
        for _g in Global.objects.all():
            g[_g.slug] = _g.value
        request.session['global'] = g

    def process_response(self, request, response):
        return response
