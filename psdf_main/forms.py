from django import forms
from .models import *

from django.core.exceptions import ValidationError
class UserForm(forms.ModelForm):
    class Meta:
        model = users
        fields = ['username', 'password', 'nodal', 'region', 'utilname', 'contact', 'address', 'email']
        # fields = '__all__'
        REGIONS = [('','Region'),('NR','NR'), ('SR','SR'),('ER','ER'),('WR','WR'),('NER','NER')]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control col-md-6 mb-3 text-center', 'placeholder' : 'Enter username', 'id' : 'username'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control col-md-6 mb-3 text-center', 'placeholder' : 'Enter password', 'id' : 'password', 'name' : 'password'}),
            'nodal' : forms.TextInput(attrs={'placeholder':'Nodal Officer','class':'form-control col-md-5 mb-3 text-center'}),
            'region' : forms.Select(attrs={'placeholder':'Region','class':'form-control col-md-3 text-center','style':'height:100%;'}, choices=REGIONS),
            'utilname' : forms.TextInput(attrs={'placeholder':'Name of Utility','class':'form-control col-md-6 mb-3 text-center', 'id':'utility'}),
            'contact' : forms.TextInput(attrs={'placeholder':'Contact Number','class':'form-control col-md-6 mb-3 text-center'}),
            'address' : forms.TextInput(attrs={'id':'address', 'class':'form-control text-center mb-3', 'placeholder':'Enter the Address','style':'height:100%;'}),
            'email' : forms.EmailInput(attrs={'id':'email', 'class':'form-control text-center mb-3 col-md-5', 'placeholder':'Enter e-mail','style':'height:100%;'})
        }


# class NewDPR_form(forms.ModelForm):
    
#     class Meta:
#         model = temp_projects
#         fields = ['proname', 'amountasked','schedule']
#         widgets = {
#             'proname' : forms.TextInput(attrs={'type':"text" ,'class':"form-control bg-gray-200 border-0 small" ,'placeholder':"Project name", 'aria-label':"Project name" ,'aria-describedby':"basic-addon2" ,'namne':"projnaem" ,'id':"projname"}),
#             'amountasked' : forms.TextInput(attrs={'type':"text" ,'class':"form-control bg-gray-200 border-0 small" ,'placeholder':"Amount (in crore Rupees upto 2 decimal places)", 'aria-label':"Requested amount" ,'aria-describedby':"basic-addon2" ,'namne':"amount" ,'id':"amount"}),
#             'schedule' : forms.TextInput(attrs={'type':"text" ,'class':"form-control bg-gray-200 border-0 small" ,'placeholder':"Schedule (in months)", 'aria-label':"Schedule " ,'aria-describedby':"basic-addon2" ,'namne':"schedule" ,'id':"schedule"}),
#         }
        
