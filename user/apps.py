from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user"

    def ready(self) -> None:
        from django.db.models.signals import post_delete
        import user.signals as signals
        from user.models import Student, Professor, Assistant

        post_delete.connect(signals.delete_instance_user, sender=Student)
        post_delete.connect(signals.delete_instance_user, sender=Professor)
        post_delete.connect(signals.delete_instance_user, sender=Assistant)
