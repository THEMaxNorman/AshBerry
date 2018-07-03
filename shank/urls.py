"""shank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from messenger import views as core_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^mainMessages', core_views.messagesMain, name = 'mainMessage'),
    url('^messages/(?P<string>[\w\-]+)/$', core_views.messageFrom, name = 'messageFrom'),
    url('^newMessages/(?P<string>[\w\-]+)/$', core_views.newMessage, name='newMessage'),
    url(r'^contacts', core_views.contacts, name = 'contacts'),
    url(r'^calc', core_views.calc, name = 'calc'),
    url('^app/(?P<string>[\w\-]+)/$', core_views.app, name='app'),
    url('^appstore/$', core_views.appStore, name = 'appStore'),
    url('^newApp/$', core_views.createNewApp, name = 'cna'),
    url('^yapp/$', core_views.yapps, name='yapp'),
    url('^pop/$', core_views.play_pop, name='pop'),
    url('^settings/$', core_views.settings, name='settings'),
    url('^makeawish/$', core_views.make_a_wish, name='makeawish'),
    url('^memeUpload/$', core_views.memeUpload, name='memeUpload'),
    url('^memeDict/$', core_views.memeDict, name='memeDict'),
    url('^meme/(?P<string>[\w\-]+)/$', core_views.meme, name='meme'),
    url('^ymeme/$', core_views.ymeme, name='ymeme'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
