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
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

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
revise="Revision Requested"
rejected="Rejected"

status_dict = {revise:-1, rejected:-2, savestatus:0, sup_propsub:1, sup_propapp:2, ody_propapp:3,
          sup_compsub:4, sup_compapp:5, ody_compapp:6}

WORD_EXTENSION = '.docx'
def viewProposal(request):
    supervisors = User.objects.filter(groups__name='Supervisors')
    return render(request, 'projects/proposal.html', {'supervisors':supervisors,
                                                      'categories':categories})

def status(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    grp = ProjectGroup.objects.filter(project=project)
    return render(request, 'projects/status.html',
                  {'project':project,
                   'statusNum':status_dict.get(project.status),
                   'group':grp})

@login_required(login_url='/odyssey/accounts/login/')
def viewAs(request):
    return render(request, 'projects/viewas.html')

def superLanding(request):
    projects = Project.objects.filter(advisor__username="goadrich")
    proposals = projects.filter(status=sup_propsub)
    completions = projects.filter(status=sup_compsub)
    inprogress = projects.exclude(status=sup_propsub).exclude(status=sup_compsub).exclude(status=ody_compapp)
    appprops = projects.filter(status=sup_propapp)
    appcomps = projects.filter(status=sup_compapp)
    odyprops = projects.filter(status=ody_propapp)
    odycomps = projects.filter(status=ody_compapp)
    groups = ProjectGroup.objects.filter(project__advisor__username="goadrich")
    return render(request, 'projects/superLanding.html', {'projects':projects,
                                                          'props':proposals,
                                                          'completions':completions,
                                                          'completed':odycomps,
                                                          'inprogress':inprogress})

def odyLanding(request):
    projects = Project.objects.exclude(status=savestatus).exclude(status=revise).exclude(status=rejected)
    proposals = projects.filter(status=sup_propapp)
    completions = projects.filter(status=sup_compapp)
    inprogress= projects.exclude(status=sup_propapp).exclude(status=sup_compapp).exclude(status=ody_compapp)
    completed = projects.filter(status=ody_compapp)
    return render(request, 'projects/odysseylanding.html', {'proposals':proposals,
                                                            'completions':completions,
                                                            'inprogress':inprogress,
                                                            'completed':completed})

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
        elif data.get('propose')=="Save Form":
            project.status=savestatus
            proposal.status=savestatus
            project.save()
            proposal.save()
            return render(request,'projects/proposalSave.html', {'project':project})
        else:
            project.delete()
            return render(request, 'projects/proposalDelete.html')
                
def editProposal(request, project_id):
    supervisors = User.objects.filter(groups__name='Supervisors')
    project = get_object_or_404(Project, pk=project_id)
    group = ProjectGroup.objects.filter(project=project)
    narrative = get_object_or_404(Proposal, project_id=project).narrative
    return render(request, 'projects/proposalEdit.html',
                  {'project':project, 'supervisors':supervisors,
                   'categories':categories, 'startdate':project.start_date.isoformat(),
                   'enddate':project.end_date.isoformat(),
                   'group':group, 'narrative':narrative})


def landing(request):
    projects = Project.objects.exclude(status=savestatus).exclude(status=revise).exclude(status=ody_compapp)
    proposals = Proposal.objects.filter(status=savestatus)
    completions = Completion.objects.filter(status=savestatus)
    revprops = Proposal.objects.filter(status=revise)
    revcomps = Completion.objects.filter(status=revise)
    complete = Project.objects.filter(status=ody_compapp)
    return render(request, 'projects/landing.html', {'projects':projects,
                                                     'proposals':proposals,
                                                     'completions':completions,
                                                     'revprops':revprops,
                                                     'revcomps':revcomps,
                                                     'completed':complete})

def viewCompletion(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    grp = ProjectGroup.objects.filter(project=project)    
    return render(request, 'projects/completion.html',
                  {'project':project,
                   'enddate':project.end_date.isoformat(),
                   'group':grp})

@csrf_protect
def submitSavedCompletion(request, project_id):
    now=datetime.date.today()
    if request.method=='POST':
        comp = get_object_or_404(Completion, pk=project_id)
        project = get_object_or_404(Project, pk=project_id)
        data=request.POST
        comp.hours=data.get('hours')
        comp.updated_date=now
        comp.notation = data.get('description')
        if data.get('complete') == "Save & Submit to Supervisor":
            project.end_date=data.get('enddate')
            project.status=sup_compsub
            project.update_date=now
            comp.status=sup_compsub
            project.save()
            comp.save()
            return render(request,'projects/success.html')
        elif data.get('complete') == "Save Form":
            project.end_date=data.get('enddate')
            comp.status=savestatus
            comp.save()
            return render(request,'projects/completionSave.html',
                          {'project':project, 'categories':categories})
        else:
            comp.delete()
            return render(request, 'projects/proposalDelete.html')
            

        

@csrf_protect
def submitCompletion(request, project_id):
    now=datetime.date.today()
    project = get_object_or_404(Project, pk=project_id)
    data = request.POST
    new_comp=Completion(project_id=project,
                        status="",
                        hours=data.get('hours'),
                        notation=data.get('description'),
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
    completion = get_object_or_404(Completion, pk=project_id)
    hours = completion.hours
    description = completion.notation
    return render(request, 'projects/completionEdit.html',
                  {'project':project, 'supervisors':supervisors,
                   'startdate':project.start_date.isoformat(),
                   'enddate':project.end_date.isoformat(),
                   'hours':hours, 'description':description})


def reviewProposal(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    grp = ProjectGroup.objects.filter(project=project)
    narrative = get_object_or_404(Proposal, project_id=project).narrative
    return render(request, 'projects/superProposal.html',
                  {'project':project, 'group':grp,
                   'narrative':narrative})

def odyReviewProposal(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    grp = ProjectGroup.objects.filter(project=project)
    narrative = get_object_or_404(Proposal, project_id=project).narrative
    return render(request, 'projects/odysseyproposal.html',
                  {'project':project, 'group':grp,
                   'narrative':narrative})

def supReviewComp(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    grp = ProjectGroup.objects.filter(project=project)
    completion = get_object_or_404(Completion, pk=project_id)
    hours = completion.hours
    desc = completion.notation
    return render(request, 'projects/superCompletion.html',
                  {'project':project, 'group':grp, 'hours':hours,
                   'description':desc})

def odyReviewComp(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    grp = ProjectGroup.objects.filter(project=project)
    completion = get_object_or_404(Completion, pk=project_id)
    hours = completion.hours
    desc = completion.notation
    return render(request, 'projects/odysseyCompletion.html',
                  {'project':project, 'group':grp, 'hours':hours,
                   'description':desc})

def supViewStatus(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    grp = ProjectGroup.objects.filter(project=project)
    return render(request, 'projects/superStatus.html',
                  {'project':project,
                   'statusNum':status_dict.get(project.status),
                   'group':grp
                   })

def odyViewStatus(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    grp = ProjectGroup.objects.filter(project=project)
    return render(request, 'projects/odysseyStatus.html',
                  {'project':project,
                   'statusNum':status_dict.get(project.status),
                   'group':grp})  

def odyAppProposal(request, project_id):
    return approve(request, project_id, ody_propapp)
    
def superAppProposal(request, project_id):
    return approve(request, project_id, sup_propapp)

def approve(request, project_id, success):
    now=datetime.date.today()
    data = request.POST
    project = get_object_or_404(Project, pk=project_id)
    proposal = get_object_or_404(Proposal, pk=project_id)
    result = data.get("approve")
    if result == "Approve Proposal":
        project.status=success
        proposal.status=success
    elif result == "Request Revision":
        project.status=revise
        proposal.status=revise
    else:
        project.status=rejected
        proposal.status=rejected
    project.update_date=now
    proposal.updated_date=now
    project.save()
    proposal.save()
    return render(request,'projects/superSuccess.html')
def supAppComp(request, project_id):
    return complete(request, project_id, sup_compapp)

def odyAppComp(request, project_id):
    return complete(request, project_id, ody_compapp)

def complete(request, project_id, success):
    now = datetime.date.today()
    data = request.POST
    project = get_object_or_404(Project, pk=project_id)
    completion = get_object_or_404(Completion, pk=project_id)
    result = data.get('complete')
    if result=='Approve Completion':
        project.status=success
        completion.status=success
    else:
        project.status=rejected
        completion.status=rejected
    project.update_date=now
    completion.updated_date = now
    project.save()
    completion.save()
    return render(request,'projects/superSuccess.html')

# USER AUTHENTICATION
def loginView(request):
    return render( request, 'projects/login.html')

@csrf_protect
def my_view(request):
    def errorHandle(error):
        return render( request, 'projects/login.html',{'error':error})

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render(request, 'projects/landing.html', {
                'username': username,
            })

        else:
            error = u'account disabled'
            return errorHandle(error)
    else:
        error = u'invalid login'
        return errorHandle(error)

def pickGroup(g):
    if g == 'Student':
        group = 'Students'
    elif g == 'Supervisor':
        group = 'Supervisors'
    elif g == 'Odyssey Staff':
        group = 'Odyssey'
    else:
        group = None
    return group

@csrf_protect
def signup(request):
    if request.method=='POST':
        data = request.POST
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(
                username,
                password,
                username # Username is also email
            )
        user.first_name = request.POST['firstname']
        user.last_name  = request.POST['lastname']
        g = pickGroup(request.POST['auth'])
        if g is not None:
            group = Group.objects.get(name=g)
            group.user_set.add(user)
        user.save()
        return redirect('views.viewAs')    
    else:
        return render(request, 'projects/createUser.html')
