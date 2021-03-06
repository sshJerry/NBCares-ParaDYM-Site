from django.contrib import admin
from .models import Event
from .models import Organization
from .models import OrgEvent
from .models import Contact

# Register your models here.
admin.site.register(Organization)
admin.site.register(Event)
admin.site.register(OrgEvent)
admin.site.register(Contact)

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