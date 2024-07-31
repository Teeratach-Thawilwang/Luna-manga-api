import re
from datetime import datetime, time, timedelta

from django.core.cache import cache
from django.http import QueryDict
from django.utils import timezone
from django.utils.text import slugify


def only(methods):
    mapMethod = {
        "index": "get",
        "show": "get",
        "store": "post",
        "update": "put",
        "destroy": "delete",
    }
    result = {}
    for method in methods:
        result[mapMethod[method]] = method
    return result


def dd(data):
    if isinstance(data, str):
        raise Exception(data)
    if isinstance(data, QueryDict):
        raise Exception(dict(data))
    if isinstance(data, dict):
        raise Exception(dict(data))
    raise Exception(list(data))


def transformStringToBoolean(text: str) -> bool:
    if text == "true" or text == "True":
        return True
    return False


def setCache(key: str, value: any, seconds: int):
    cache.set(key, value, seconds)


def getCache(key: str, default=None):
    return cache.get(key, default)


def getDatetimeTodayUtc():
    toDayUtc = timezone.now().date()
    return datetime.combine(toDayUtc, time.min, tzinfo=timezone.utc)


def getSecondsUntilTomorrow():
    now = timezone.now()
    tomorrow = datetime.combine(now.date() + timedelta(days=1), time.min, tzinfo=timezone.utc)
    delta = tomorrow - now
    return int(delta.total_seconds())


def extractEnglish(text: str):
    englishText = re.findall(r"[a-zA-Z]+", text)
    return " ".join(englishText)


def createSlug(text: str):
    text = extractEnglish(text)
    return slugify(text, allow_unicode=True)
