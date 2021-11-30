from django.apps import AppConfig


class ProjectsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ProjectSite'

    def ready(self):
        import ProjectSite.signals
