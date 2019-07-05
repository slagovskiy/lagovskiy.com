"""odyssey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .settings import MEDIA_ROOT, MEDIA_URL
from .media.views import media

urlpatterns = [
    # JWT auth
    url(r'^api/v1/auth/obtain_token/', obtain_jwt_token),
    url(r'^api/v1/auth/refresh_token/', refresh_jwt_token),

    # The rest of the endpoints
    #url(r'^api/v1/', include('project.api', namespace='apiv1')),

    url(r'^api/v1/user/', include('odyssey.userext.urls')),
    url(r'^api/v1/blog/', include('odyssey.blog.urls')),
    url(r'^api/v1/media/', include('odyssey.media.urls')),

    url(r'^media/(?P<path>.*)$', media),

    path('admin/', admin.site.urls),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
