from atexit import register
from django.apps import AppConfig
from django.conf import settings




class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    # def ready(self):
    #     configs = getattr(settings, "CKEDITOR_CONFIGS", None)
    #     if configs and configs.get("versionCheck"):
    #         register(check_ckeditor_version)