from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .forms import ProjectForms, OrganizationEventForm, AdminUserCreation
from .models import Event, Organization, OrgEvent
from .filters import OrgEventFilter
from .decorators import allowed_users


def view_home(request):
    return render(request, 'ProjectSite/home.html')


def view_about(request):
    return render(request, 'ProjectSite/about.html')


def view_contacts(request):
    return render(request, 'ProjectSite/contacts.html')


def view_organization_user(request):
    context = {}
    return render(request, 'ProjectSite/organization-user.html', context)


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
    #form = OrganizationEventForm(instance=orgevents)

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
def view_admin_user_creation(request):
    form = AdminUserCreation()
    if request.method == 'POST':
        form = ProjectForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
        else:
            form = AdminUserCreation(instance=form)

    context = {'form': form}
    render(request, 'ProjectSite/admin-user-creation.html', context)