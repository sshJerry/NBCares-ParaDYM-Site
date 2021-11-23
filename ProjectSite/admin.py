from django.contrib import admin
from .models import Event
from .models import Tag
from .models import Organization
from .models import OrgEvent

# Register your models here.
admin.site.register(Organization)
admin.site.register(Tag)
admin.site.register(Event)
admin.site.register(OrgEvent)