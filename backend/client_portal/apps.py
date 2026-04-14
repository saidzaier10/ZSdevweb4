from django.apps import AppConfig


class ClientPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client_portal'
    verbose_name = 'Espace client'

    def ready(self):
        from django.db.models.signals import post_save
        from .models import ProjectUpdate, ClientProject
        from .signals import on_project_update_created, on_client_project_saved
        post_save.connect(on_project_update_created, sender=ProjectUpdate)
        post_save.connect(on_client_project_saved, sender=ClientProject)
