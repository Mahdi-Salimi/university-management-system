import random
import string


def generate_otp(length=6):
    return "".join(random.choices(string.digits, k=length))


def change_pass_otp_redis_key_generator(user):
    return "change_pass_" + user.email + "_" + str(user.id)
