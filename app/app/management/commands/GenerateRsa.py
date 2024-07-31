from app.Settings.path import STORAGE_DIR, env
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate RSA"

    def handle(self, *args, **kwargs):
        pass_phrase = bytes(env("SECRET_KEY"), "utf-8")
        private_Key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())

        with open(STORAGE_DIR + "private_key.pem", "wb") as fb:
            fb.write(
                private_Key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.BestAvailableEncryption(pass_phrase),
                )
            )

        public_key = private_Key.public_key()
        with open(STORAGE_DIR + "public_key.pem", "wb") as fb:
            fb.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )
