from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views import generic
from django.template import loader
from .models import *
from django.contrib.auth.models import User, Group

def proposal(request):
    supervisors = User.objects.filter(groups__name='Supervisors')
    return render(request, 'projects/proposal.html', {'supervisors':supervisors})

def landing(request):
    projects = Project.objects.all()
    return render(request, 'projects/landing.html', {'projects':projects})

def completion(request):
    return render(request, 'projects/completion.html')
