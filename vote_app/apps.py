from django.apps import AppConfig


class VoteAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vote_app'
    
    def ready(self):
        from experation_scheduler import updater
        updater.start()