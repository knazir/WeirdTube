import search.views

from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^$', search.views.index, name='index'),
    url(r'^search', search.views.search, name='search'),
    url(r'^admin/', include(admin.site.urls)),
]
