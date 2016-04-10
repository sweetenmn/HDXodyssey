from django import forms
from .models import Project
from django.contrib.auth.models import User


class SubmitProposal(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'category', 'advisor']
        widgets = {
            'title' : forms.TextInput(attrs={'id':'title',
                                             'required':True,
                                             'placeholder':'Title'}),
            'category' : forms.TextInput(attrs={'id':'category','required':True,
                                                'placeholder':'Category'})
            }
            
        
