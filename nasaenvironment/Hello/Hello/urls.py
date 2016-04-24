"""Hello URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from Hello.views import hello,current_datetime,hours_ahead
from temp import views as temp_views
import settings

urlpatterns = [
    url(r'^$', temp_views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^hello/$',hello),
    url(r'^time/$',current_datetime),
    url(r'^time/plus/(\d{1,2})/$',hours_ahead),
	url(r'^temp/',temp_views.temp,name='temp'),
	url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root':settings.STATIC_PATH }),
	url(r'^data-visualization.html/$',temp_views.datavisualization,name="data-visualization"),
	url(r'^temppng.html/$',temp_views.temppng,name="temppng"),
	url(r'^maps.html/$',temp_views.maps,name="maps"),
]
