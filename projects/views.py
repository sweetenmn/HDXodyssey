from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.views import generic
from django.template import loader
from .models import *
from django.contrib.auth.models import User, Group
from .forms import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from os.path import basename
import datetime

import logging
logger = logging.getLogger(__name__)

def proposal(request):
    supervisors = User.objects.filter(groups__name='Supervisors')
    return render(request, 'projects/proposal.html', {'supervisors':supervisors})

@csrf_protect
def status(request, project_id):
    if request.method=='POST':
        project = get_object_or_404(Project, pk=project_id)
        return render(request, 'projects/status.html', {'project':project})

@csrf_protect
def upload(request):
    if request.method == 'POST':
        logger.debug(request.POST['text'])
        handle_uploaded_file(request.FILES['descfile'])
        return HttpResponseRedirect('success')
    return render(request, 'completion')

def handle_uploaded_file(f):
    with open('projects/uploadedfiles/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@csrf_protect
def success(request):
    return render(request, 'projects/success.html')
    

@csrf_protect
def submit(request):
    now=datetime.datetime.now()
    if request.method == 'POST':
        if 'narfile' in request.FILES:
            handle_uploaded_file(request.FILES['narfile'])
        data = request.POST
        new_project=create_project(data)
        create_proposal(data, new_project)
        create_group(new_project)
        return HttpResponseRedirect('success')
    return render(request, 'projects/success.html')

@csrf_protect
def submit_saved(request, project_id):
    if request.method == 'POST':
        if 'narfile' in request.FILES:
            handle_uploaded_file(request.FILES['narfile'])
        data = request.POST
        

def edit_proposal(request):

def edit_completion(request):

def create_project(data):
    new_title = data.get('title')
    adv = data.get('super')
    new_adv = User.objects.get(pk=adv)
    new_category = data.get('cat')
    new_project=Project(title=new_title, category=new_category,
                        advisor=new_adv, status="Proposed", start_date="4/16/2016",
                        end_date="4/16/2016", update_date="4/16/2016")
    new_project.save()
    return new_project

def create_proposal(data, project):
    new_prop=Proposal(project_id=project, narrative=data.get('narrative'),
                      created_date=now, status="Submitted to supervisor",
                      updated_date=now)
    new_prop.save()

def create_group(project):
    new_grp = ProjectGroup(student=User.objects.get(username='jepsencr'),
                                   project=project)
    new_grp.save()
    
@csrf_protect
def save(request):
    if request.method=='POST':
        if 'narfile' in request.FILES:
            handle_uploaded_file(request.FILES['narfile'])
        data=request.POST
        
def landing(request):
    projects = Project.objects.all()
    return render(request, 'projects/landing.html', {'projects':projects})

def completion(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/completion.html', {'project':project})
