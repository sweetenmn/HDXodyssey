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
import pypandoc
from io import *
from docx import Document

import logging
logger = logging.getLogger(__name__)

WORD_EXTENSION = '.docx'
def proposal(request):
    supervisors = User.objects.filter(groups__name='Supervisors')
    return render(request, 'projects/proposal.html', {'supervisors':supervisors})

def status(request, project_id):
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
    with open(f.name, 'wb+') as destination:
        source_stream = StringIO(f.read())
        document = Document(source_stream)
        source_stream.close()
        # for chunk in f.chunks():
        #     destination.write(chunk)
        # handle_word_file(destination, f.name)

def handle_word_file(f, fileName):
    # Convert Docx file to Markdown for storage
    docName = 'clone'+fileName
    document = Document(f)
    document.save(docName)
    output_filename = 'TEST.md'
    md_source = pypandoc.convert(docName, 'md', outputfile= output_filename) # Return this string for now
@csrf_protect
def success(request):
    return render(request, 'projects/success.html')


@csrf_protect
def submit(request):
    substatus="Sumbitted to Supervisor"
    savestatus="Unsubmitted"
    now=datetime.datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if 'narfile' in request.FILES:
            handle_uploaded_file(request.FILES['narfile'])
        data = request.POST
        new_title = data.get('title')
        adv = data.get('super')
        new_adv = User.objects.get(pk=adv)
        new_category = data.get('cat')
        
        new_project=Project(title=new_title,
                            category=new_category,
                            advisor=new_adv,
                            status="",
                            start_date=data.get('startdate'),
                            end_date=data.get('enddate'),
                            update_date=now
                            ) 
        new_prop=Proposal(project_id=new_project,
                          narrative=data.get('narrative'),
                          created_date=now,
                          status="",
                          updated_date=now
                          )
        if data.get('propose')=="Save & Submit to Supervisor":
            new_project.status=substatus
            new_prop.status=substatus
            new_project.save()
            new_prop.save()
            
            return render(request, 'projects/success.html')
        else:
            new_project.status=savestatus
            new_prop.status=savestatus
            new_project.save()
            new_prop.save()
            return render(request,'projects/proposalSave.html', {'project':new_project})
            
@csrf_protect
def submit_saved(request, project_id):
    substatus="Sumbitted to Supervisor"
    savestatus="Unsubmitted"
    now=datetime.datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if 'narfile' in request.FILES:
            handle_uploaded_file(request.FILES['narfile'])
        data = request.POST
        new_title = data.get('tatle')
        adv = data.get('super')
        new_adv = User.objects.get(pk=adv)
        new_category = data.get('cat')
        
        new_project=Project(title=new_title,
                            category=new_category,
                            advisor=new_adv,
                            status="",
                            start_date=data.get('startdate'),
                            end_date=data.get('enddate'),
                            update_date=now
                            ) 
        new_prop=Proposal(project_id=new_project,
                          narrative=data.get('narrative'),
                          created_date=now,
                          status="",
                          updated_date=now
                          )
        if data.get('propose')=="Save & Submit to Supervisor":
            new_project.status=substatus
            new_prop.status=substatus
            new_project.save()
            new_prop.save()
            
            render(request, 'projects/success.html')
        else:
            new_project.status=savestatus
            new_prop.status=savestatus
            new_project.save()
            new_prop.save()
            return render(request,'projects/proposalSave.html', {'project':new_project})
                
    

def edit_proposal(request, project_id):
    supervisors = User.objects.filter(groups__name='Supervisors')
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/proposalEdit.html',
                  {'project':project, 'supervisors':supervisors})
    

def landing(request):
    projects = Project.objects.all()
    proposals = Proposal.objects.all()
    return render(request, 'projects/landing.html', {'projects':projects, 'proposals':proposals})

def completion(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/completion.html', {'project':project})
