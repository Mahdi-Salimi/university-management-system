def user_image_path(instance, filename):
    ext = filename.split(".")[-1]
    return f"user_images/user_{instance.username}.{ext}"
