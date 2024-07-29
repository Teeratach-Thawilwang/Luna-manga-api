from app.Domain.Configuration.Models.Configuration import Configuration
from app.Settings.configurations import configurations as configurationsConfigs


class ConfigurationSeeder:
    def create(self):
        configurations = Configuration.objects.values_list("key", flat=True)
        for configuration in configurationsConfigs:
            if configuration["key"] not in configurations:
                Configuration.objects.create(**configuration)

        configsKeyList = [config["key"] for config in configurationsConfigs]
        Configuration.objects.exclude(key__in=configsKeyList).delete()
