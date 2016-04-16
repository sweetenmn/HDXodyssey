from django.conf.urls import url
from . import views

app_name = 'projects'
urlpatterns = [url(r'^$', views.landing, name = 'landing'),
               url(r'^proposal/', views.proposal, name = 'proposal'),
               url(r'^complete-project/(?P<project_id>[0-9]+)', views.completion, name = 'completion'),
               url(r'^project-status/(?P<project_id>[0-9]+)',views.status, name='status'),
               url(r'^proposal/submit_proposal/$', views.submit_proposal, name='submit_proposal'),
               url(r'^upload/$', views.upload, name='upload'),
               url(r'^upload/success', views.success, name='success'),
               ]
