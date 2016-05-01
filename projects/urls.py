from django.conf.urls import url
from . import views
from django.contrib.auth import views as supervisor
from django.contrib.auth import views as oydssey

app_name = 'projects'
urlpatterns = [url(r'^$', views.landing, name = 'landing'),
               url(r'^proposal/$', views.proposal, name = 'proposal'),
               url(r'^complete-project/(?P<project_id>[0-9]+)', views.completion, name = 'completion'),
               url(r'^project-status/(?P<project_id>[0-9]+)',views.status, name='status'),
               url(r'^proposal/submit/', views.submit, name='submit'),
               url(r'^upload/$', views.upload, name='upload'),
               url(r'^upload/success', views.success, name='success'),
               url(r'^success', views.success, name='success'),
               url(r'^edit-form/(?P<project_id>[0-9]+)/$', views.edit_proposal, name='edit'),
               url(r'^edit-form/(?P<project_id>[0-9]+)/submit', views.submitsaved, name='submitedit'),
               url(r'^Login/$', views.login, name = 'Login'),
 			   url(r'^Supervisor-page/$', views.superLanding, name = 'superLanding'),
 			   url(r'^superProposal/$', views.superProposal, name = 'superProposal'),
			   url(r'^odysseylanding/$', views.odysseylanding, name = 'odysseylanding'),
			   url(r'^odysseyproposal/$', views.odysseyproposal, name = 'odysseyproposal'),
			   ]
               
			   
