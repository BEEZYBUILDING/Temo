from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'orders'

    def ready(self):
        import orders.signals #this tells djanngo to load signals when the app starts