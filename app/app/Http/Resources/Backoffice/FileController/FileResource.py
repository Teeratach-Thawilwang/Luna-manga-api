import json

from app.Services.LocalTime import localTime
from django.http import JsonResponse


class FileResource(JsonResponse):
    def __init__(self, file, status=200, safe=False, json_dumps_params=None, **kwargs):
        conversion = file.conversion
        if conversion is not None:
            conversion = json.loads(conversion)

        self.data = {
            "id": file.id,
            "uuid": file.uuid,
            "file_name": file.file_name,
            "mime_type": file.mime_type,
            "collection_name": file.collection_name,
            "conversion": conversion,
            "created_at": localTime(file.created_at),
            "updated_at": localTime(file.updated_at),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
