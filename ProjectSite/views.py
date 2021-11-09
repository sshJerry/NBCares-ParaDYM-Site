from django.shortcuts import render, redirect
from .forms import ProjectForms
from .models import ProjectSite
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

    events = ProjectSite.objects.all()
    context = {'events': events, 'event_add': event_add}
    return render(request, 'ProjectSite/events.html', context)


def update_events(request, event_id):
    event = ProjectSite.objects.get(id=event_id)

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
    event = ProjectSite.objects.get(id=event_id)
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
    context = {'login_form' : login_form}
    return render(request, 'ProjectSite/login.html', context)


def view_logout(request):
    logout(request)
    return redirect('home')


def view_settings(request):
    return render(request, 'ProjectSite/settings.html')
