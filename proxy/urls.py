from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from proxy import views

urlpatterns = [
                  url(r'(?P<project>.*)/start$', views.job_start),
                  url(r'^$', views.project, name='project'),
                  url(r'^project/getall$', views.project_getall),
                  url(r'^project/getdetail$', views.project_getdetail),
                  url(r'^project/add$', views.project_add),
                  url(r'^project/update$', views.project_update),
                  url(r'^project/delete$', views.project_delete),
                  url(r'^job$', views.job, name='job'),
                  url(r'^job/getall/(?P<number>\d+)$', views.job_getall, ),
                  url(r'^lab$', views.lab, name='lab'),
                  url(r'^lab/getall$', views.lab_getall),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
