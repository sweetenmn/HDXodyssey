from django.conf.urls import url
from . import views

app_name = 'projects'
urlpatterns = [url(r'^student/', views.landing, name = 'landing'),
               url(r'^supervisor/', views.superLanding, name='superLanding'),
               url(r'^$', views.viewAs, name = 'viewas'),
               url(r'^proposal/$', views.viewProposal, name = 'proposal'),
               url(r'^complete-project/(?P<project_id>[0-9]+)/$', views.
                   viewCompletion, name = 'completion'),
               url(r'^project-status/(?P<project_id>[0-9]+)',
                   views.status, name='status'),
               url(r'^proposal/submit/', views.submitProposal, name='submit'),
               url(r'^upload/$', views.upload, name='upload'),
               url(r'^upload/success', views.success, name='success'),
               url(r'^success', views.success, name='success'),
               url(r'^edit-form/(?P<project_id>[0-9]+)/$',
                   views.editProposal, name='edit'),
               url(r'^edit-form/(?P<project_id>[0-9]+)/submit',
                   views.submitSavedProposal, name='submitedit'),
               url(r'^edit-completion-form/(?P<project_id>[0-9]+)/submit',
                   views.submitSavedCompletion, name='submitcompleteedit'),
               url(r'^complete-project/(?P<project_id>[0-9]+)/submit',
                   views.submitCompletion, name='submitcompletion'),
               url(r'^edit-completion-form/(?P<project_id>[0-9]+)/$',
                   views.editCompletion, name='editcomp'),
               
               ]
