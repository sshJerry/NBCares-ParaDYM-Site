import django_filters
from django_filters import DateFilter, CharFilter

from .models import *


class OrgEventFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="org_event_date_created", lookup_expr='gte')
    end_date = DateFilter(field_name="org_event_date_created", lookup_expr='lte')

    class Meta:
        model = OrgEvent
        fields = '__all__'
        exclude = ['org_event_organization', 'org_event_date_created']


class ContactFilter(django_filters.FilterSet):
    class Meta:
        model = Contact
        fields = ['services']
        exclude = ['contact_resource_provider', 'contact_ages', 'contact_websites', 'contact_location',
                   'contact_number']


class CalendarFilter(django_filters.FilterSet):
    nameContains = CharFilter(field_name='event_name', lookup_expr='icontains')
    eventContains = CharFilter(field_name='event_description', lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['event_tag']
