from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from proxy import views

urlpatterns = [
                  url(r'(?P<project>.*)/start', views.job_start),
                  url(r'^$', views.project, name='project'),
                  url(r'^project/getall$', views.project_getall),
                  url(r'^project/getdetail$', views.project_getdetail),
                  url(r'^project/add$', views.project_add),
                  url(r'^project/update$', views.project_update),
                  url(r'^project/delete$', views.project_delete),
                  url(r'^test/log/(?P<logid>\d+)/$', views.test_run_log),
                  url(r'^job$', views.job, name='job'),
                  url(r'^job/getall/(?P<number>\d+)$', views.job_getall),
                  url(r'^lab$', views.lab, name='lab'),
                  url(r'^lab/getall$', views.lab_getall),
                  url(r'^report/(?P<logid>\d+)/$', views.test_log),
                  url(r'^report/(?P<logid>\d+)/log.html$', views.test_log),
                  url(r'^report/(?P<logid>\d+)/report.html$', views.test_report),
                  url(r'^report/(?P<logid>\d+)/cache/(?P<cid>\d+\.\d+\.txt)$', views.test_cache),
                  url(r'^report/(?P<logid>\d+)/compare/(?P<cid>\d+\.\d+\.html)$', views.test_compare),
                  url(r'^report/(?P<logid>\d+)/compare/deps/(?P<redfile>.+)$', views.test_redfile),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
