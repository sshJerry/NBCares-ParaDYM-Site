from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjectForms
from .models import Event, Organization, OrgEvent
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout


def view_home(request):
    return render(request, 'ProjectSite/home.html')


def view_about(request):
    return render(request, 'ProjectSite/about.html')


def view_contacts(request):
    return render(request, 'ProjectSite/contacts.html')


def view_events(request):
    event_add = ProjectForms()
    if request.method == 'POST':
        event_add = ProjectForms(request.POST)
        if event_add.is_valid():
            event_add.save()
            return redirect('events')

    events = Event.objects.all()
    context = {'events': events, 'event_add': event_add}
    return render(request, 'ProjectSite/events.html', context)


def update_events(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.method == 'POST':
        event_form = ProjectForms(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            return redirect('events')
    else:
        event_form = ProjectForms(instance=event)
    context = {'event_form': event_form}
    return render(request, 'ProjectSite/events-update.html', context)


def delete_events(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('events')
    context = {'event': event}
    return render(request, 'ProjectSite/events-delete.html', context)


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


def view_settings(request):
    return render(request, 'ProjectSite/settings.html')


def view_admin(request):
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
    return render(request, 'ProjectSite/admin.html', context)


def view_admin_organzation(request, pk):
    org = Organization.objects.get(id=pk)
    #orgevents = org.order_by.all()
    orgevents = org.orgevent_set.all()

    context = {'org': org, 'orgevents': orgevents}
    return render(request, 'ProjectSite/admin-organization.html',context)
