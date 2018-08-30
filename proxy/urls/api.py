from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from proxy import views

urlpatterns = [
                  url(r'^project/getall$', views.project_getall),
                  url(r'^node/list/$', views.project_getallnodes),
                  url(r'^project/getdetail$', views.project_getdetail),
                  url(r'^project/save$', views.project_save),
                  url(r'^project/new$', views.project_add),
                  url(r'^project/delete$', views.project_delete),
                  url(r'^job/log/(?P<logid>\d+)/$', views.test_run_log),
                  url(r'^job/getall$', views.job_getall),
                  url(r'^job/(?P<project>[\w-]*)/start', views.job_start),
                  url(r'^job/(?P<project>[\w-]*)/stop', views.job_stop),
                  url(r'^job/(?P<jobpk>[\w-]*)/rerun', views.job_rerun),
                  url(r'^lab/getall$', views.lab_getall),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
