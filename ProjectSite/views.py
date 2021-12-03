from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse
from .forms import ProjectForms, OrganizationEventForm, AdminUserCreation, AdminUserCreationAdditionalFields
from .models import *
from .filters import OrgEventFilter, ContactsFilters
from .decorators import allowed_users


def view_home(request):
    return render(request, 'ProjectSite/home.html')


def view_about(request):
    return render(request, 'ProjectSite/about.html')


def view_contacts(request):
    allcontacts = Contact.objects.all()
    conFilters = ContactsFilters(request.GET, queryset=allcontacts)
    filtered_contacts = conFilters.qs
    context = {'allcontacts':allcontacts, 'filtered_contacts':filtered_contacts, 'conFilters':conFilters}
    return render(request, 'ProjectSite/contacts.html', context)


def view_events(request):
    orgevents = OrgEvent.objects.all()
    completed_events = orgevents.filter(org_event_status='Accepted')

    event_add = ProjectForms()
    if request.method == 'POST':
        event_add = ProjectForms(request.POST)
        if event_add.is_valid():
            event_add.save()
            return redirect('events')

    events = Event.objects.all()
    context = {'events': events, 'event_add': event_add, 'completed_events': completed_events}
    return render(request, 'ProjectSite/events.html', context)


def view_login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')
    else:
        login_form = AuthenticationForm()
    context = {'login_form': login_form}
    return render(request, 'ProjectSite/login.html', context)


def view_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def create_events(request, pk):
    EventFormSet = inlineformset_factory(Organization, OrgEvent, fields=('org_event_event', 'org_event_status'),
                                         extra=1)
    organization = Organization.objects.get(id=pk)
    formset = EventFormSet(queryset=OrgEvent.objects.none(), instance=organization)
    # form = OrganizationEventForm(initial={'org_event_organization': organization})

    if request.method == 'POST':
        # form = OrganizationEventForm(request.POST)
        formset = EventFormSet(request.POST, instance=organization)
        if formset.is_valid():
            formset.save()
            return redirect('admin_panel')
    context = {'formset': formset}
    return render(request, 'ProjectSite/events-create.html', context)


@login_required(login_url='login')
def update_events(request, pk):
    orgevents = OrgEvent.objects.get(id=pk)
    # form = OrganizationEventForm(instance=orgevents)

    if request.method == 'POST':
        form = OrganizationEventForm(request.POST, instance=orgevents)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = OrganizationEventForm(instance=orgevents)

    context = {'form': form}
    return render(request, 'ProjectSite/events-update.html', context)


@login_required(login_url='login')
def delete_events(request, pk):
    form = OrgEvent.objects.get(id=pk)
    if request.method == 'POST':
        form.delete()
        return redirect('admin_panel')
    context = {'form': form}
    return render(request, 'ProjectSite/events-delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def view_admin_panel(request):
    orgevents = OrgEvent.objects.all()
    orgs = Organization.objects.all()

    total_orgs = orgs.count()
    total_events = orgevents.count()
    pending_events = orgevents.filter(org_event_status='Waiting Approval').count()
    completed_events = orgevents.filter(org_event_status='Accepted').count()

    context = {'orgs': orgs, 'orgevents': orgevents,
               'total_orgs': total_orgs, 'total_events': total_events,
               'pending_events': pending_events, 'completed_events': completed_events
               }
    return render(request, 'ProjectSite/admin-panel.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def view_admin_organzation(request, pk):
    org = Organization.objects.get(id=pk)
    # orgevents = org.order_by.all()
    orgevents = org.orgevent_set.all()
    orgevents_count = orgevents.count()

    OrganizationEventFilter = OrgEventFilter(request.GET, queryset=orgevents)
    orgevents = OrganizationEventFilter.qs
    context = {'org': org, 'orgevents': orgevents, 'orgevents_count': orgevents_count,
               'OrganizationEventFilter': OrganizationEventFilter}
    return render(request, 'ProjectSite/admin-organization.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def view_admin_user_creation(request, *args, **kwargs):
    user_form = AdminUserCreation()
    if request.method == 'POST':
        user_form = AdminUserCreation(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            """group = Group.objects.get(name='organizer')
            user.groups.add(group)
            Organization.objects.create(user=user, org_name=user.username)"""
            return redirect('home')
    context = {'user_form': user_form}
    return render(request, 'ProjectSite/admin-user-creation.html', context)


"""  
    user_form = AdminUserCreation()
    org_form = AdminUserCreationAdditionalFields()

    if request.method == 'POST':
        user_form = AdminUserCreation(request.POST)
        #org_form = AdminUserCreationAdditionalFields(request.POST)

        if user_form.is_valid() and org_form.is_valid():
            user = user_form.save()
            group = Group.objects.get(name='organizer')
            user.groups.add(group)
            user.refresh_from_db()

            #org_form = AdminUserCreationAdditionalFields(request.POST,instance=profile)
            org_form.full_clean() #Moved to top
            profile.user.org_name = profile.POST.get('org_name')
            profile.user.org_address = org_form.get('org_address')
            profile.user.org_phone = org_form.get('org_phone')
            profile.user.org_email = org_form.get('org_email')
            profile.user.save()
            #org_form.full_clean()
            #org_form.save()
            return redirect('home')
    context = {'user_form': user_form, 'org_form': org_form}
    return render(request, 'ProjectSite/admin-user-creation.html', context)"""


# else:form = AdminUserCreation(instance=form)

# org_form = AdminUserCreationAdditionalFields(request.POST, instance=user)
# Makes ONE Organization Object, Users with no Organization information populated

# org_form = AdminUserCreationAdditionalFields(request.POST)
# Makes Two Organization Objects, One with user and organization information empty, Other without user
# and organization information populated


@login_required(login_url='login')
def view_organization_events(request):
    org = Organization.objects.get(user=request.user)
    orgevents = org.orgevent_set.all()

    context = {'orgevents': orgevents}
    return render(request, 'ProjectSite/organization_events.html', context)


def view_organization_settings(request):
    organ = request.user.organization
    form = AdminUserCreationAdditionalFields(instance=organ)
    if request.method == 'POST':
        form = AdminUserCreationAdditionalFields(request.POST, instance=organ)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'ProjectSite/organization-settings.html', context)


######################### CALENDAR #########################
from django.views import generic
from .forms import ProjectForms
from .models import Event
from datetime import datetime


class view_calendar(generic.View):
    class_form = ProjectForms

    def get(self, request, *args, **kwargs):
        forms = self.class_form()
        events = Event.objects.all()
        print('Events\t\t\t: ' + str(events))
        event_list = []
        for event in events:
            print('Events List\t\t\t: ' + str(event.event_sTime.date()))
            print('Events List WITH TIME\t\t\t: ' + str(event.event_sTime.date().strftime("%Y-%m-%dT%H:%M:%S")))
            event_list.append(
                {
                    "title": event.event_name,
                    "start": event.event_sTime.date().strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.event_eTime.date().strftime("%Y-%m-%dT%H:%M:%S"),
                }
            )
        context = {'form': forms, 'events': event_list}
        print('POST  List\t\t\t: ' + str(event_list))
        return render(request, 'ProjectSite/calendar-template.html', context)

    def post(self, request, *args, **kwargs):
        forms = self.class_form(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('events')
        context = {"form": forms}
        return render(request, 'ProjectSite/calendar-template.html', context)