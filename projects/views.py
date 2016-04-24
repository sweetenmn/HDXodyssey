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
from django.core.mail import send_mail
from django.core import mail


def proposal(request):
    supervisors = User.objects.filter(groups__name='Supervisors')
    return render(request, 'projects/proposal.html', {'supervisors':supervisors})

def status(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/status.html', {'project':project})
    
    
def submit_proposal(request):
    if request.method == 'POST':
        new_title = request.POST.get('title')
        adv = request.POST.get('super')
        new_advisor = User.objects.get(pk=adv[3:])
        new_category = request.POST.get('category')
        response_data = {}
        project = Project(title=new_title, category=new_category,
                          advisor=new_advisor, status="Incomplete")
        project.save()
        response_data['result'] = 'Create project successful'
        response_data['projectpk'] = project.pk
        response_data['title']=project.title
        response_data['advisor']=project.advisor
        response_data['category']=project.category
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def landing(request):
    projects = Project.objects.all()
    return render(request, 'projects/landing.html', {'projects':projects})

def completion(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/completion.html', {'project':project})




    
