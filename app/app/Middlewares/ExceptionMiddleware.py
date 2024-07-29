import json
from datetime import datetime, timezone

from app.Settings.path import env
from django.http import HttpResponse, JsonResponse
from rest_framework import status


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # if env("APP_ENV") == "test":
        #     return self.createResponse(str(exception))
        # return exception.__dict__
        print(exception)
        return self.createResponse(str(exception))

    def isJson(self, string):
        try:
            json.loads(string)
            return True
        except ValueError as e:
            return False

    def convertDatetimeStringToString(self, data):
        startWord = "datetime.datetime("
        stopWord = ", tzinfo=datetime.timezone.utc)"
        lenStartWord = len(startWord)
        lenStopWord = len(stopWord)

        while startWord in data and stopWord in data:
            dateStartIndex = data.find(startWord)
            dateStopIndex = data.find(stopWord)

            datetimeList = data[dateStartIndex + lenStartWord : dateStopIndex].split(", ")
            datetimeParam = [int(value) for value in datetimeList]

            datetimeObject = datetime(*datetimeParam, tzinfo=timezone.utc)
            date = '"' + datetimeObject.strftime("%Y-%m-%dT%H:%M:%SZ") + '"'
            data = data.replace(data[dateStartIndex : dateStopIndex + lenStopWord], date)

        return data

    def createResponse(self, data):
        data = data.replace("'", '"')
        data = self.convertDatetimeStringToString(data)

        if self.isJson(data):
            try:
                jsonData = json.loads(data)
                statusCode = status.HTTP_400_BAD_REQUEST
                if "code" in jsonData:
                    statusCode = jsonData["code"]
                    del jsonData["code"]
                return JsonResponse(jsonData, safe=False, status=statusCode)
            except Exception as e:
                return HttpResponse(e)
        return HttpResponse(data, status=status.HTTP_400_BAD_REQUEST)
