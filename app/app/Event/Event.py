from app.Enums.EventEnum import EventEnum
from app.Listener.BannerListener import BannerListener
from app.Listener.StorageListener import StorageListener


class Event:
    def __init__(self, event, params):
        match event:
            case EventEnum.UPLOAD_FILE:
                StorageListener().upload(**params)

            case EventEnum.DELETE_FILE:
                StorageListener().delete(**params)

            case EventEnum.SYNC_BANNER_FILEABLE:
                BannerListener().syncFileable(**params)
