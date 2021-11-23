from django.forms import ModelForm
from .models import OrgEvent, Organization


class AdminUserCreation(ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        exclude = ['org_date_created']


class OrganizationEventForm(ModelForm):
    class Meta:
        model = OrgEvent
        fields = '__all__'

from django import forms
from .models import Event


class ProjectForms(forms.ModelForm):
    CHOICES = (('None', 'None'), ('Toddler', 'Toddler'),
               ('Child', 'Child'), ('Adolescent', 'Adolescent'), ('Adult', 'Adult'),
               ('Elderly', 'Elderly'), ('Other', 'Other'))

    class Meta:
        model = Event
        fields = '__all__'

    widgets = {
        'event-name': forms.TextInput(attrs={'class': 'form-control'}),
        'event-date': forms.TextInput(attrs={'class': 'form-control'}),
        'event-sTime': forms.TextInput(attrs={'class': 'form-control'}),
        'event-eTime': forms.TextInput(attrs={'class': 'form-control'}),
        'event-description': forms.TextInput(attrs={'class': 'form-control'}),
        'event-tag': forms.Select(attrs={'class': 'form-select'}, choices=CHOICES),
    }
