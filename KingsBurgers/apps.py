from django.apps import AppConfig


class KingsburgersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'KingsBurgers'

    def ready(self):
        # Import se�ales o configuraciones necesarias al iniciar la app
        pass
