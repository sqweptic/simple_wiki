from django.conf.urls import patterns, url
from wiki.views import IndexPage, Page, EditPage, AddPage, DeletePage

urlpatterns = patterns('', 
                      url(r'^$', IndexPage.as_view(), name='index'),
                      url(r'^add/$', AddPage.as_view(), name='add_base'),
                      url(r'^(?P<page>.+)/delete/$', DeletePage.as_view(), name='delete'),
                      url(r'^(?P<page>.+)/add/$', AddPage.as_view(), name='add'),                      
                      url(r'^(?P<page>.+)/edit/$', EditPage.as_view(), name='edit'),
                      url(r'^(?P<page>.+)/$', Page.as_view(), name='page'),
)