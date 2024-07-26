from app.Enums.AudioMimeTypeEnum import AudioMimeTypeEnum
from app.Enums.DocumentMimeTypeEnum import DocumentMimeTypeEnum
from app.Enums.ImageMimeTypeEnum import ImageMimeTypeEnum
from app.Enums.VideoMimeTypeEnum import VideoMimeTypeEnum


class CollectionEnum:
    BANNER_STORY = {
        "mimetypes": ImageMimeTypeEnum.list(),
        "conversion": {
            "thumbnail": {
                "width": 160,
                "height": "auto",
            },
        },
    }

    BANNER_CHAPTER = {
        "mimetypes": ImageMimeTypeEnum.list(),
        "conversion": {
            "thumbnail": {
                "width": 160,
                "height": "auto",
            },
        },
    }

    BANNER_STORY_WINDOW_1 = {
        "mimetypes": ImageMimeTypeEnum.list(),
        "conversion": {
            "thumbnail": {
                "width": 200,
                "height": 200,
            },
            "desktop": {
                "width": 1000,
                "height": 1000,
            },
        },
    }

    BANNER_STORY_WINDOW_2 = {
        "mimetypes": ImageMimeTypeEnum.list(),
        "conversion": {
            "thumbnail": {
                "width": 196,
                "height": 94,
            },
            "desktop": {
                "width": 980,
                "height": 470,
            },
        },
    }

    BANNER_STORY_WINDOW_3 = {
        "mimetypes": ImageMimeTypeEnum.list(),
        "conversion": {
            "thumbnail": {
                "width": 196,
                "height": 94,
            },
            "desktop": {
                "width": 980,
                "height": 470,
            },
        },
    }

    BANNER_ADVERTISEMENT_SMALL = {
        "mimetypes": ImageMimeTypeEnum.list(),
        "conversion": {
            "thumbnail": {
                "width": 196,
                "height": 60,
            },
            "desktop": {
                "width": 980,
                "height": 300,
            },
        },
    }

    BANNER_ADVERTISEMENT_MEDIUM = {
        "mimetypes": ImageMimeTypeEnum.list(),
        "conversion": {
            "thumbnail": {
                "width": 200,
                "height": 50,
            },
            "desktop": {
                "width": 1000,
                "height": 250,
            },
        },
    }

    BANNER_ADVERTISEMENT_GROUP = {
        "mimetypes": ImageMimeTypeEnum.list(),
        "conversion": {
            "thumbnail": {
                "width": 200,
                "height": 36,
            },
            "desktop": {
                "width": 1000,
                "height": 180,
            },
        },
    }

    PROFILE_IMAGE = {
        "mimetypes": ImageMimeTypeEnum.list(),
        "conversion": {
            "thumbnail": {
                "width": 160,
                "height": "auto",
            },
            "desktop": {
                "width": 1000,
                "height": "auto",
            },
        },
    }

    STORY_IMAGE = {
        "mimetypes": ImageMimeTypeEnum.list(),
        "conversion": {
            "thumbnail": {
                "width": 160,
                "height": "auto",
            },
        },
    }

    CHAPTER_COVER_IMAGE = {
        "mimetypes": ImageMimeTypeEnum.list(),
        "conversion": {
            "thumbnail": {
                "width": 160,
                "height": "auto",
            },
        },
    }

    CATEGORY_IMAGE = {
        "mimetypes": ImageMimeTypeEnum.list(),
        "conversion": {
            "thumbnail": {
                "width": 160,
                "height": "auto",
            },
            "desktop": {
                "width": 1000,
                "height": "auto",
            },
        },
    }

    CHAPTER_AUDIO = {
        "mimetypes": AudioMimeTypeEnum.all(),
        "conversion": None,
    }

    VIDEO = {
        "mimetypes": VideoMimeTypeEnum.all(),
        "conversion": None,
    }

    DOCUMENT = {
        "mimetypes": DocumentMimeTypeEnum.all(),
        "conversion": None,
    }

    def get(self, collection):
        collection = collection.upper()
        collections = self.all()
        if collection not in collections:
            return None

        return {"name": collection.lower(), **collections[collection]}

    def all(self):
        return {
            "BANNER_STORY": self.BANNER_STORY,
            "BANNER_CHAPTER": self.BANNER_CHAPTER,
            "BANNER_STORY_WINDOW_1": self.BANNER_STORY_WINDOW_1,
            "BANNER_STORY_WINDOW_2": self.BANNER_STORY_WINDOW_2,
            "BANNER_STORY_WINDOW_3": self.BANNER_STORY_WINDOW_3,
            "BANNER_ADVERTISEMENT_SMALL": self.BANNER_ADVERTISEMENT_SMALL,
            "BANNER_ADVERTISEMENT_MEDIUM": self.BANNER_ADVERTISEMENT_MEDIUM,
            "BANNER_ADVERTISEMENT_GROUP": self.BANNER_ADVERTISEMENT_GROUP,
            "PROFILE_IMAGE": self.PROFILE_IMAGE,
            "STORY_IMAGE": self.STORY_IMAGE,
            "CHAPTER_COVER_IMAGE": self.CHAPTER_COVER_IMAGE,
            "CATEGORY_IMAGE": self.CATEGORY_IMAGE,
            "CHAPTER_AUDIO": self.CHAPTER_AUDIO,
            "VIDEO": self.VIDEO,
            "DOCUMENT": self.DOCUMENT,
        }


class CollectionNameEnum:
    BANNER_STORY = "banner_story"
    BANNER_CHAPTER = "banner_chapter"
    BANNER_STORY_WINDOW_1 = "banner_story_window_1"
    BANNER_STORY_WINDOW_2 = "banner_story_window_2"
    BANNER_STORY_WINDOW_3 = "banner_story_window_3"
    BANNER_ADVERTISEMENT_SMALL = "banner_advertisement_small"
    BANNER_ADVERTISEMENT_MEDIUM = "banner_advertisement_medium"
    BANNER_ADVERTISEMENT_GROUP = "banner_advertisement_group"
    PROFILE_IMAGE = "profile_image"
    STORY_IMAGE = "story_image"  # story cover image, chapter image (manga image)
    CHAPTER_COVER_IMAGE = "chapter_cover_image"
    CATEGORY_IMAGE = "category_image"
    CHAPTER_AUDIO = "chapter_audio"
    VIDEO = "video"
    DOCUMENT = "document"

    @staticmethod
    def list(by="key"):
        if by == "key":
            return [item.lower() for item in list(CollectionEnum().all().keys())]
        return list(CollectionEnum().all().values())
