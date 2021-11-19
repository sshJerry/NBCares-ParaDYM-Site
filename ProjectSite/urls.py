from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_home, name="home"),
    path('events', views.view_events, name="events"),
    path('about', views.view_about, name="about"),
    path('contacts', views.view_contacts, name="contacts"),
    path('login', views.view_login, name="login"),
    path('logout', views.view_logout, name='logout'),
    path('setting', views.view_settings, name="settings"),
    path('update/<int:event_id>', views.update_events, name="update_events"),
    path('delete/<int:event_id>', views.delete_events, name="delete_events"),
    path('admin', views.view_admin, name="admin"),
    path('admin_organization/<str:pk>', views.view_admin_organzation, name="admin_organization"),
]