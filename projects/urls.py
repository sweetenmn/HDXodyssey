from django.conf.urls import url
from . import views

app_name = 'projects'
urlpatterns = [url(r'^$', views.landing, name = 'landing'),
               url(r'^proposal/', views.proposal, name = 'proposal'),
               url(r'^completion/', views.completion, name = 'completion'),
               url(r'^proposal/submit_proposal/$', views.submit_proposal, name='submit_proposal'),
               ]
