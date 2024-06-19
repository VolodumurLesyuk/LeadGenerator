from django import forms
from .models import WorkerLead, EmployeeLead


class WorkerLeadForm(forms.ModelForm):
    class Meta:
        model = WorkerLead
        fields = ['name', 'phone', 'comment', 'customer']
        exclude = ['customer']


class EmployeeLeadForm(forms.ModelForm):
    class Meta:
        model = EmployeeLead
        fields = ['name', 'phone', 'comment', 'customer']
        exclude = ['customer']
