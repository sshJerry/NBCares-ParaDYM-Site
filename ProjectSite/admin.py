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

"""from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Organization
    exclude = ['org_status']
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)"""