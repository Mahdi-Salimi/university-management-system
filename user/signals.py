from rest_framework.fields import ObjectDoesNotExist


def delete_instance_user(sender, instance, **kwargs):
    try:
        if instance.user:
            try:
                instance.user.delete()
            except Exception:
                pass
    except ObjectDoesNotExist:
        pass
