from typing import Any

from app.Domain.Configuration.Models.Configuration import Configuration
from app.Exceptions.ResourceNotFoundException import ResourceNotFoundException
from django.db.models.query import QuerySet
from django.utils import timezone


class ConfigurationService:
    def findBy(self, params: dict[str, Any]) -> QuerySet:
        return Configuration.objects.filter(**params)

    def findByKey(self, key: str) -> Configuration:
        return Configuration.objects.filter(**{"key": key}).first()

    def create(self, params: dict[str, Any]) -> Configuration:
        return Configuration.objects.create(**params)

    def update(self, id: int, params: dict[str, Any]) -> Configuration:
        params["updated_at"] = timezone.now()
        try:
            Configuration.objects.filter(pk=id).update(**params)
            return Configuration.objects.get(pk=id)
        except Exception as e:
            raise ResourceNotFoundException({"message": e})

    def deleteById(self, id: int) -> None:
        try:
            configuration = Configuration.objects.get(pk=id)
            configuration.delete()
        except Exception as e:
            raise ResourceNotFoundException({"message": e})
