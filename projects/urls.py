from django.conf.urls import url
from . import views

app_name = 'projects'
urlpatterns = [
          url(
               r'^student/$', 
               views.landing, 
               name = 'landing'
          ),
          url(
               r'^supervisor/$', 
               views.superLanding, 
               name='superLanding'
          ),
          url(
               r'^$', 
               views.viewAs, 
               name = 'viewas'
          ),
          url(
               r'^proposal/$', 
               views.viewProposal, 
               name = 'proposal'
          ),
          url(
               r'^student/complete-project/(?P<project_id>[0-9]+)/$', 
               views.viewCompletion, 
               name = 'completion'
          ),
          url(
               r'^student/project-status/(?P<project_id>[0-9]+)',
               views.status, 
               name='status'
          ),
          url(
               r'^student/proposal/submit/', 
               views.submitProposal, 
               name='submit'
          ),
          url(
               r'^upload/$', 
               views.upload, 
               name='upload'
          ),
          url(
               r'^upload/success', 
               views.success, 
               name='success'
          ),
          url(
               r'^success', 
               views.success, 
               name='success'
          ),
          url(
               r'^student/edit-form/(?P<project_id>[0-9]+)/$',
               views.editProposal, 
               name='edit'
          ),
          url(
               r'^student/edit-form/(?P<project_id>[0-9]+)/submit',
               views.submitSavedProposal, 
               name='submitedit'
          ),
          url(
               r'^student/edit-completion-form/(?P<project_id>[0-9]+)/submit',
               views.submitSavedCompletion, 
               name='submitcompleteedit'
          ),
          url(
               r'^student/complete-project/(?P<project_id>[0-9]+)/submit',
               views.submitCompletion, 
               name='submitcompletion'
          ),
          url(
               r'^student/edit-completion-form/(?P<project_id>[0-9]+)/$',
               views.editCompletion, 
               name='editcomp'
          ),
          url(
               r'^supervisor/review-proposal/(?P<project_id>[0-9]+)/$', 
               views.reviewProposal,
               name='superprop'
          ),
          url(
               r'^supervisor/review-proposal/(?P<project_id>[0-9]+)/submit',
               views.superAppProposal, 
               name='superapp'
          ),
          url(
               r'^accounts/login/$', 
               views.loginView
          ),
          url(
               r'^accounts/login/submit/', 
               views.my_view
          ),
          url(r'^office/review-proposal/(?P<project_id>[0-9]+)/$', views.odyReviewProposal,
                   name='odyReviewProp'),
          url(r'^office/review-proposal/(?P<project_id>[0-9]+)/submit',
                   views.odyAppProposal, name='odyapp'),
               
     ]
