from django import forms
from .models import ProjectSite


class ProjectForms(forms.ModelForm):
    CHOICES = (('None', 'None'), ('Toddler', 'Toddler'),
               ('Child', 'Child'), ('Adolescent', 'Adolescent'), ('Adult', 'Adult'),
               ('Elderly', 'Elderly'), ('Other', 'Other'))

    class Meta:
        model = ProjectSite
        fields = '__all__'

    widgets = {
        'event-name': forms.TextInput(attrs={'class': 'form-control'}),
        'event-date': forms.TextInput(attrs={'class': 'form-control'}),
        'event-sTime': forms.TextInput(attrs={'class': 'form-control'}),
        'event-eTime': forms.TextInput(attrs={'class': 'form-control'}),
        'event-description': forms.TextInput(attrs={'class': 'form-control'}),
        'event-tag': forms.Select(attrs={'class': 'form-select'}, choices=CHOICES),
    }
