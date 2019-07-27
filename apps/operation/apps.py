from django.apps import AppConfig


class OperationConfig(AppConfig):
    name = 'operation'
    def ready(self):
        import operation.signals
