"""media_player URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from media_player.views import hello, homepage_view, current_datetime, video_player, audio_media_browser, video_media_browser, canvas_video, trailers, local_video_player
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', current_datetime),
	url(r'^video/$', video_player),
	url(r'^audio_media/$', audio_media_browser),
	url(r'^video_media/$', video_media_browser),
	url(r'^local_video_player/$', local_video_player),
	url(r'^canvas/$', canvas_video),
	url(r'^$', homepage_view),
    	url(r'^admin/', admin.site.urls),
    	url(r'^trailers/$', trailers),
    	url(r'^hello/$', hello),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
 
