import functools
import json


def RequestParserMiddleware(next):
    @functools.wraps(next)
    def wrapper(request, *args, **kwargs):
        requestBody = {}
        id = {}

        content_type = request.headers.get("Content-Type", "").lower()
        if content_type.startswith("multipart/form-data"):
            requestBody = request.POST.dict()

        elif request.body:
            requestBody = json.loads(request.body)

        if request.method == "PUT":
            idxStart = request.path_info.rfind("/") + 1
            id = {"id": request.path_info[idxStart:]}

        request.params = {**requestBody, **request.GET, **id, **request.FILES}
        return next(request, *args, **kwargs)

    return wrapper
