from django.utils import timezone


def localTime(dateTime, formatString="%Y-%m-%d %H:%M:%S"):
    if dateTime:
        return timezone.localtime(dateTime).strftime(formatString)

    return None
