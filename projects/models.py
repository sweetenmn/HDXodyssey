from django.db import models
from django.contrib.auth.models import User, Group
##should be using get_user_model()
##https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#referencing-the-user-model
class Project(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20)
    advisor = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=60)
    start_date = models.DateField('start date')
    end_date = models.DateField('end date')
    update_date = models.DateField('updated on')
    def __str__(self):
        return self.title

class ProjectGroup(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    def __str__(self):
        return self.project.title+": "+self.student.first_name+" "+self.student.last_name
    class Meta:
        unique_together = (("student", "project"),)

def user_dir_path(instance, filename):
    return 'proposals/project_{0}/{1}'.format(instance.project_id, (filename+'%Y-%m-%d'))
    
class Proposal(models.Model):
    project_id = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True)
    narrative = models.CharField(max_length=2000)
    created_date = models.DateField('created on')
    status = models.CharField(max_length=60)
    updated_date = models.DateField('updated on')
    def __str__(self):
        return self.project_id.title


class Completion(models.Model):
    project_id = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True)
    status = models.CharField(max_length=60)
    created_date = models.DateField('created on')
    updated_date = models.DateField('updated on')
    notation = models.CharField(max_length=500)
    def __str__(self):
<<<<<<< HEAD
        return "Completion: " + self.project.id.title

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    stu_ID = models.CharField(max_length=100)
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name

class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    sup_ID = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name

class Odyssey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    ody_ID = models.CharField(max_length=100)
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name
=======
        return "Completion: " + self.project_id.title
>>>>>>> refs/remotes/origin/master
