from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

handler404 = 'wiki.views.error404'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'test_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)), 
    url(r'^wiki/', include('wiki.urls')),
)
