import re
from datetime import datetime, time, timedelta

from django.core.cache import cache
from django.http import QueryDict
from django.utils import timezone
from django.utils.text import slugify

from app.Enums.CachePagePrefixEnum import CachePagePrefixEnum


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
    toDayLocalTime = timezone.localtime(timezone.now())
    midnightLocalTime = toDayLocalTime.replace(hour=0, minute=0, second=0, microsecond=0)
    midnightUTC = midnightLocalTime.astimezone(timezone.utc)
    return midnightUTC


def getSecondsUntilTomorrow():
    midnightUTC = getDatetimeTodayUtc()
    tomorrow = midnightUTC + timedelta(days=1)
    delta = tomorrow - timezone.now()
    return int(delta.total_seconds())


def extractEnglish(text: str):
    englishText = re.findall(r"[a-zA-Z]+", text)
    return " ".join(englishText)


def createSlug(text: str):
    text = extractEnglish(text)
    return slugify(text, allow_unicode=True)


def getReferer(request):
    return request.META.get("HTTP_REFERER", "")


def getUserAgent(request):
    return request.META.get("HTTP_USER_AGENT", "")


def getUserIPAddress(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


def getRequestMeta(request):
    return {
        "referer": getReferer(request),
        "user_agent": getUserAgent(request),
        "ip_address": getUserIPAddress(request),
    }


def clearAllRedisCacheByKeyPrefix(keyPrefix: CachePagePrefixEnum):
    cache.delete_pattern(f"*{keyPrefix}*")


def flushCache():
    cache.clear()
