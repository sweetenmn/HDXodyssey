from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views import generic
from django.template import loader
from .models import *
from django.contrib.auth.models import User, Group

def index(request):
    template = loader.get_template('projects/index.html')
    supervisors = User.objects.filter(groups__name='Supervisors')
    
    return render(request, 'projects/index.html', {'supervisors':supervisors})
