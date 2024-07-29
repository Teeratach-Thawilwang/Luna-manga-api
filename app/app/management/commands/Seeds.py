from app.management.Services.ConfigurationSeeder import ConfigurationSeeder
from app.management.Services.CustomerGroupSeeder import CustomerGroupSeeder
from app.management.Services.CustomerSeeder import CustomerSeeder
from app.management.Services.OAuthClientSeeder import OAuthClientSeeder
from app.management.Services.PermissionSeeder import PermissionSeeder
from app.management.Services.UserSeeder import UserSeeder
from django.core.management.base import BaseCommand

"""
To run command
shell  run => python manage.py Seeds <seeder>
docker run => docker-compose exec app python manage.py Seeds <seeder>
"""


class Command(BaseCommand):
    help = "Seed Data"

    def add_arguments(self, parser):
        parser.add_argument("Seeder", type=str, help="The name of factory model.", nargs="?", default="all")
        parser.add_argument("Quality", type=int, help="The number of generated record.", nargs="?", default=1)

    def handle(self, *args, **kwargs):
        seeder = kwargs["Seeder"]
        quality = kwargs["Quality"]

        match seeder:
            case "initial":
                ConfigurationSeeder().create()
                PermissionSeeder().create()
                UserSeeder().create(isSuperUser=True)
                OAuthClientSeeder().create()
                CustomerGroupSeeder().create()
                CustomerSeeder().create()
            case "user":
                UserSeeder().create(quality=quality)
            case "configuation":
                ConfigurationSeeder().create()
            case "permission":
                PermissionSeeder().create()
