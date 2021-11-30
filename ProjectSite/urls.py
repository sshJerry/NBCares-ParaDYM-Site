from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_home, name="home"),
    path('events', views.view_events, name="events"),
    path('about', views.view_about, name="about"),
    path('contacts', views.view_contacts, name="contacts"),
    path('login', views.view_login, name="login"),
    path('logout', views.view_logout, name='logout'),
    path('create/<str:pk>', views.create_events, name="create_events"),
    path('update/<str:pk>', views.update_events, name="update_events"),
    path('delete/<str:pk>', views.delete_events, name="delete_events"),
    path('admin-panel', views.view_admin_panel, name="admin_panel"),
    path('admin-organization/<str:pk>', views.view_admin_organzation, name="admin_organization"),
    path('admin-user-creation', views.view_admin_user_creation, name="admin_user_creation"),
    path('organization-events', views.view_organization_events, name="organization_events"),
    path('organization-settings', views.view_organization_settings, name="organization_settings"),
    path('calendar-template/', views.view_calendar.as_view(), name="calendar"),
]