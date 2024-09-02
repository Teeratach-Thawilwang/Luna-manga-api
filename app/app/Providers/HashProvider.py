from django.contrib.auth.hashers import PBKDF2PasswordHasher


class HashProvider(PBKDF2PasswordHasher):
    algorithm = "sha1"
    iterations = 10000
