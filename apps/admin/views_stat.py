from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext

from apps.admin.utils import *
from apps.admin.views import custom_proc


def stat_index(request):
    if not check_access(request.user, 'canAdmin'):
        return HttpResponseRedirect('/admin/ad/')
    message = ''
    t = loader.get_template('admin/blog/category.html')
    c = RequestContext(
        request,
        {
            'message': message,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))