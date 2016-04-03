from django.db import models
from django.contrib.auth.models import User, Group
##should be using get_user_model()
##https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#referencing-the-user-model
class Project(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20)
    advisor = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    
class ProjectGroup(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    def __str__(self):
        return self.project.title+": "+self.student.first_name+" "+self.student.last_name
    class Meta:
        unique_together = (("student", "project"),)


class Proposal(models.Model):
    project_id = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True)
    narrative = models.CharField(max_length=500)
    created_date = models.DateTimeField('created on')
    status = models.CharField(max_length=20)
    updated_date = models.DateTimeField('updated on')
    def __str__(self):
        return self.project_id.title
