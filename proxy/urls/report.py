from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from proxy import views

urlpatterns = [url(r'^test/log/(?P<logid>\d+)/$', views.test_run_log),
               url(r'^report/(?P<logid>\d+)/$', views.test_log),
               url(r'^report/(?P<logid>\d+)/log.html$', views.test_log),
               url(r'^report/(?P<logid>\d+)/report.html$', views.test_report),
               url(r'^report/(?P<logid>\d+)/output.xml$', views.test_xml),
               url(r'^report/(?P<logid>\d+)/cache/(?P<cid>\d+\.\d+\.txt)$', views.test_cache),
               url(r'^report/(?P<logid>\d+)/cache/(?P<cid>\d+.txt)$', views.test_cache),
               url(r'^report/(?P<logid>\d+)/compare/(?P<cid>\d+\.\d+\.html)$', views.test_compare),
               url(r'^report/(?P<logid>\d+)/compare/(?P<cid>\d+\.html)$', views.test_compare),
               url(r'^report/(?P<logid>\d+)/compare/deps/(?P<redfile>.+)$', views.test_redfile),
               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
