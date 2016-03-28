from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)

class Advisor(models.Model):
    name = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class Project(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20)
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)

class Group(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    class Meta:
        unique_together = (("student", "project"),)

class Proposal(models.Model):
    project_id = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True)
    narrative = models.CharField(max_length=500)
    created_date = models.DateTimeField('created on')
    status = models.CharField(max_length=20)
    updated_date = models.DateTimeField('updated on')

