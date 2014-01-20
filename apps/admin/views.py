from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.contrib.auth import authenticate, login, logout


def custom_proc(request):
    return {
        'app_title': 'Admin',
        'link_app': 'admin',
        #'link_category': '',
        #'link_tag': '',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],
        'ajax': request.GET.get('ajax', 0)
    }


def index(request):
    message = ''
    t = loader.get_template('admin/default.html')
    c = RequestContext(
        request,
        {
            'message': message,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def login_action(request):
    message = ''
    t = loader.get_template('admin/login.html')
    c = RequestContext(
        request,
        {
            'message': message,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))


def login_check(request):
    _login = request.POST.get('txtLogin', '')
    _password = request.POST.get('txtPassword', '')
    page = request.POST.get('return', '/')
    if page is None:
        page = '/'
    user = authenticate(username=_login, password=_password)
    if user is not None:
        if user.is_active:
            login(request, user)
    return HttpResponseRedirect(page)


def logout_action(request):
    page = request.META.get('HTTP_REFERER')
    if page is None:
        page = '/'
    logout(request)
    return HttpResponseRedirect(page)


def ad(request):
    message = ''
    t = loader.get_template('admin/access_denied.html')
    c = RequestContext(
        request,
        {
            'message': message,
        },
        processors=[custom_proc])
    return HttpResponse(t.render(c))