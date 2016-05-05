from django.shortcuts import render, redirect, get_object_or_404
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
from django.core.mail import send_mail


import logging
logger = logging.getLogger(__name__)
categories = ['Artistic Creativity', 'Global Awareness',
              'Professional and Leadership Development',
              'Special Projects', 'Service to the World',
              'Undergraduate Research']

savestatus="Unsubmitted"
sup_propsub="Proposal Submitted to Supervisor"
sup_propapp="Proposal Approved by Supervisor"
ody_propapp="Proposal Approved by Odyssey Office"
sup_compsub="Completion Form Submitted to Supervisor"
sup_compapp="Completion Form Approved by Supervisor"
ody_compapp="Completion Form Approved by Odyssey Office"

status_dict = {savestatus:0, sup_propsub:1, sup_propapp:2, ody_propapp:3,
          sup_compsub:4, sup_compapp:5, ody_compapp:6}

WORD_EXTENSION = '.docx'
def viewProposal(request):
    supervisors = User.objects.filter(groups__name='Supervisors')
    return render(request, 'projects/proposal.html', {'supervisors':supervisors,
                                                      'categories':categories})

def status(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/status.html', {'project':project,
                                                    'statusNum':status_dict.get(project.status)})

def viewAs(request):
    return render(request, 'projects/viewas.html')

def superLanding(request):
    projects = Project.objects.filter(advisor__username="goadrich")
    proposals = projects.filter(status=sup_propsub)
    completions = projects.filter(status=sup_compsub)
    inprogress = projects.exclude(status=sup_propsub).exclude(status=sup_compsub).exclude(status=ody_compapp)
    odycomps = projects.filter(status=ody_compapp)
    groups = ProjectGroup.objects.filter(project__advisor__username="goadrich")
    return render(request, 'projects/superLanding.html', {'projects':projects,
                                                          'props':proposals,
                                                          'comps':completions,
                                                          'completed':odycomps,
                                                          'inprogress':inprogress})

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
def submitProposal(request):
    now=datetime.date.today()
    if request.method == 'POST':
        if 'narfile' in request.FILES:
            handle_uploaded_file(request.FILES['narfile'])

        data = request.POST
        new_title = data.get('title')
        adv = data.get('super')
        new_adv = User.objects.get(pk=adv)
        new_category = data.get('cat')
        # handle empty date for S&S in jquery
        start = data.get('startdate')
        end = data.get('enddate')
        if start == '':
            start = now
        if end == '':
            end = now
        new_project=Project(title=new_title,
                            category=new_category,
                            advisor=new_adv,
                            status="",
                            start_date=start,
                            end_date=end,
                            update_date=now
                            )
        
        new_project.save()
        createGroup(data, new_project)
        new_prop=Proposal(project_id=new_project,
                          narrative=data.get('narrative'),
                          created_date=now,
                          status="",
                          updated_date=now
                          )
        
        new_prop.save()
        if data.get('propose')=="Save & Submit to Supervisor":
            new_project.status=sup_propsub
            new_prop.status=sup_propsub
            new_project.save()
            new_prop.save()            
            return render(request, 'projects/success.html')
        else:
            new_project.status=savestatus
            new_prop.status=savestatus
            new_project.save()
            new_prop.save()
            return render(request,'projects/proposalSave.html', {'project':new_project, 'categories':categories})

def createGroup(data, project):
    num = data.get('groupsize')
    size= int(num)
    ind = ProjectGroup(student=User.objects.get(username="jepsencr"),
                       project=project)
    ind.save()
    if size > 0:
        for i in range(size):
            mail = data.get('group-'+str(i+1))
            grp = ProjectGroup(student=User.objects.get(email=mail),
                               project=project)
            grp.save()
        
            
@csrf_protect
def submitSavedProposal(request, project_id):
    now=datetime.date.today()
    if request.method == 'POST':
        if 'narfile' in request.FILES:
            handle_uploaded_file(request.FILES['narfile'])
        project = get_object_or_404(Project, pk=project_id)
        proposal = get_object_or_404(Proposal, pk=project_id)
        data = request.POST
        uploaded_file = None
        if 'narfile' in request.FILES:
            uploaded_file = request.FILES['narfile']
            print( type(uploaded_file))

        project.title = data.get('title')
        project.advisor = User.objects.get(pk=data.get('super'))
        project.category = data.get('editcat')
        project.status=""
        project.start_date = data.get('startdate')
        project.end_date = data.get('enddate')
        project.update_date = now
        proposal.narrative=data.get('narrative')
        proposal.updated_date=now
        proposal.status=""
        if data.get('propose')=="Save & Submit to Supervisor":
            project.status=sup_propsub
            proposal.status=sup_propsub
            project.save()
            proposal.save()
            return render(request, 'projects/success.html')
        else:
            project.status=savestatus
            proposal.status=savestatus
            project.save()
            proposal.save()
            return render(request,'projects/proposalSave.html', {'project':project})
                
def editProposal(request, project_id):
    supervisors = User.objects.filter(groups__name='Supervisors')
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/proposalEdit.html',
                  {'project':project, 'supervisors':supervisors,
                   'categories':categories, 'startdate':project.start_date.isoformat(),
                   'enddate':project.end_date.isoformat()})
    
def landing(request):
    projects = Project.objects.all()
    proposals = Proposal.objects.filter(status__startswith='Unsubmitted')
    completions = Completion.objects.filter(status__startswith='Unsubmitted')
    return render(request, 'projects/landing.html', {'projects':projects,
                                                     'proposals':proposals,
                                                     'completions':completions})

def viewCompletion(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/completion.html', {'project':project})

@csrf_protect
def submitSavedCompletion(request, project_id):
    now=datetime.date.today()
    if request.method=='POST':
        comp = get_object_or_404(Completion, pk=project_id)
        project = get_object_or_404(Project, pk=project_id)
        data=request.POST
        comp.notation=""
        comp.updated_date=now
        if data.get('complete') == "Save & Submit to Supervisor":
            project.status=sup_compsub
            project.update_date=now
            comp.status=sup_compsub
            project.save()
            comp.save()
            return render(request,'projects/success.html')
        else:
            comp.status=savestatus
            comp.save()
            return render(request,'projects/completionSave.html', {'project':project, 'categories':categories})
            

        

@csrf_protect
def submitCompletion(request, project_id):
    now=datetime.date.today()
    project = get_object_or_404(Project, pk=project_id)
    data = request.POST
    new_comp=Completion(project_id=project, status="", notation="",
                        created_date=now,
                        updated_date=now)
    if data.get('complete') == "Save & Submit to Supervisor":
        project.status=sup_compsub
        project.update_date=now
        new_comp.status=sup_compsub
        project.save()
        new_comp.save()
        return render(request,'projects/success.html')
    else:
        new_comp.status=savestatus
        project.save()
        new_comp.save()
        return render(request,'projects/completionSave.html', {'project':project})

@csrf_protect    
def editCompletion(request, project_id):
    supervisors = User.objects.filter(groups__name='Supervisors')
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/completionEdit.html',
                  {'project':project, 'supervisors':supervisors,
                   'startdate':project.start_date.isoformat(),
                   'enddate':project.end_date.isoformat()})
    
def reviewProposal(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    grp = ProjectGroup.objects.filter(project=project)
    return render(request, 'projects/superProposal.html',
                  {'project':project, 'group':grp})
def superAppProposal(request, project_id):
    now=datetime.date.today()
    data = request.POST
    project = get_object_or_404(Project, pk=project_id)
    proposal = get_object_or_404(Proposal, pk=project_id)
    result = data.get("approve")
    if result == "Approve Proposal":
        project.status=sup_propapp
        project.update_date=now
        proposal.status=sup_propapp
        proposal.updated_date=now
    project.save()
    proposal.save()
    return render(request,'projects/superSuccess.html')
