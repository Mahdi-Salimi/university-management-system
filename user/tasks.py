from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail
import redis
from utils.auth import generate_otp, change_pass_otp_redis_key_generator

REDIS = settings.REDIS


@shared_task
def send_otp_task(email, otp):
    message = f"Your verification code to reset your password is: {otp}"
    send_mail("Password Reset Request", message, "noreply@golestan.invalid", [email])
    return otp


def send_change_pass_otp(user):
    otp = generate_otp()
    redis_client = redis.StrictRedis(host=REDIS["host"], port=REDIS["port"], db=REDIS["db"])
    redis_client.set(change_pass_otp_redis_key_generator(user), otp, ex=300)
    send_otp_task.delay(user.email, otp)


def verify_change_pass_otp(user, sent_otp):
    redis_client = redis.StrictRedis(host=REDIS["host"], port=REDIS["port"], db=REDIS["db"])
    key = change_pass_otp_redis_key_generator(user)
    stored_otp = redis_client.get(key)
    if stored_otp:
        if sent_otp == stored_otp.decode("utf-8"):
            redis_client.delete(key)
            return True
    return False
