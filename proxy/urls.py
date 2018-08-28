from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from proxy import views

urlpatterns = [
                  url(r'(?P<project>[\w-]*)/start', views.job_start),
                  url(r'(?P<project>[\w-]*)/stop', views.job_stop),
                  url(r'^project/getall/$', views.project_getall),
                  url(r'^node/list/$', views.project_getallnodes),
                  url(r'^project/getdetail$', views.project_getdetail),
                  url(r'^project/save$', views.project_save),
                  url(r'^project/add$', views.project_add),
                  url(r'^project/delete$', views.project_delete),
                  url(r'^test/log/(?P<logid>\d+)/$', views.test_run_log),
                  url(r'^job/log/(?P<logid>\d+)/$', views.test_run_log),
                  url(r'^job/(?P<project>[\w-]*)/$', views.job_project),
                  url(r'^job/getall/(?P<number>\d+)$', views.job_getall),
                  url(r'^job/search/(?P<project>[\w-]*)/$', views.job_search),
                  url(r'^job/search/(?P<project>[\w-]*)/(?P<number>\d+)/$', views.job_search_number),
                  url(r'^lab/getall$', views.lab_getall),
                  url(r'^lab/(?P<project>[\w-]*)/$', views.lab_project),
                  url(r'^lab/get/(?P<project>[\w-]*)/$', views.lab_getproject),
                  url(r'^report/(?P<logid>\d+)/$', views.test_log),
                  url(r'^report/(?P<logid>\d+)/log.html$', views.test_log),
                  url(r'^report/(?P<logid>\d+)/report.html$', views.test_report),
                  url(r'^report/(?P<logid>\d+)/cache/(?P<cid>\d+\.\d+\.txt)$', views.test_cache),
                  url(r'^report/(?P<logid>\d+)/cache/(?P<cid>\d+.txt)$', views.test_cache),
                  url(r'^report/(?P<logid>\d+)/compare/(?P<cid>\d+\.\d+\.html)$', views.test_compare),
                  url(r'^report/(?P<logid>\d+)/compare/(?P<cid>\d+\.html)$', views.test_compare),
                  url(r'^report/(?P<logid>\d+)/compare/deps/(?P<redfile>.+)$', views.test_redfile),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
