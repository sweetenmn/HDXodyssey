from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views import generic
from django.template import loader

def index(request):
    template = loader.get_template('projects/index.html')
    
    return HttpResponse(template.render(request))
