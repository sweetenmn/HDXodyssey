from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'projects'
<<<<<<< HEAD
urlpatterns = [
               url(r'^$', views.landing, name = 'landing'),
               url(r'^proposal/$', views.proposal, name = 'proposal'),
               url(r'^complete-project/(?P<project_id>[0-9]+)', views.completion, name = 'completion'),
               url(r'^project-status/(?P<project_id>[0-9]+)',views.status, name='status'),
               url(r'^proposal/submit/', views.submit, name='submit'),
               url(r'^upload/$', views.upload, name='upload'),
               url(r'^upload/success', views.success, name='success'),
               url(r'^success', views.success, name='success'),
               url(r'^edit-form/(?P<project_id>[0-9]+)/$', views.edit_proposal, name='edit'),
               url(r'^edit-form/(?P<project_id>[0-9]+)/submit', views.submitsaved, name='submitedit'),
               url(r'^accounts/login/$', views.loginView),
               url(r'^accounts/login/submit/', views.my_view),
               url(r'^Supervisor-page/$', views.superLanding, name = 'superLanding'),
               url(r'^Supervisor-proposal/$', views.superProposal, name = 'superProposal'),
               url(r'^Odyssey-page/$', views.odysseylanding, name = 'odysseylanding'),
               url(r'^Odyssey-proposal/$', views.odysseyproposal, name = 'odysseyproposal'),
=======
urlpatterns = [url(r'^student/$', views.landing, name = 'landing'),
               url(r'^supervisor/$', views.superLanding, name='superLanding'),
               url(r'^$', views.viewAs, name = 'viewas'),
               url(r'^proposal/$', views.viewProposal, name = 'proposal'),
               url(r'^student/complete-project/(?P<project_id>[0-9]+)/$', views.
                   viewCompletion, name = 'completion'),
               url(r'^student/project-status/(?P<project_id>[0-9]+)',
                   views.status, name='status'),
               url(r'^student/proposal/submit/', views.submitProposal, name='submit'),
               url(r'^upload/$', views.upload, name='upload'),
               url(r'^upload/success', views.success, name='success'),
               url(r'^success', views.success, name='success'),
               url(r'^student/edit-form/(?P<project_id>[0-9]+)/$',
                   views.editProposal, name='edit'),
               url(r'^student/edit-form/(?P<project_id>[0-9]+)/submit',
                   views.submitSavedProposal, name='submitedit'),
               url(r'^student/edit-completion-form/(?P<project_id>[0-9]+)/submit',
                   views.submitSavedCompletion, name='submitcompleteedit'),
               url(r'^student/complete-project/(?P<project_id>[0-9]+)/submit',
                   views.submitCompletion, name='submitcompletion'),
               url(r'^student/edit-completion-form/(?P<project_id>[0-9]+)/$',
                   views.editCompletion, name='editcomp'),
               url(r'^supervisor/review-proposal/(?P<project_id>[0-9]+)/$', views.reviewProposal,
                   name='superprop'),
               url(r'^supervisor/review-proposal/(?P<project_id>[0-9]+)/submit',
                   views.superAppProposal, name='superapp')
                   
               
>>>>>>> refs/remotes/origin/master
               ]
