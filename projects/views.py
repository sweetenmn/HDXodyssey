from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views import generic

# Create your views here.

class IndexView(generic.DetailView):
    template_name = 'projects/index.html'
