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
