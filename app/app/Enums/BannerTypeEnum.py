class BannerTypeEnum:
    STORY = "story"
    STORY_WINDOW = "story_window"
    CHAPTER = "chapter"
    ADVERTISEMENT_SMALL = "advertisement_small"
    ADVERTISEMENT_MEDIUM = "advertisement_medium"
    ADVERTISEMENT_GROUP = "advertisement_group"

    @staticmethod
    def list():
        return [
            "story",
            "story_window",
            "chapter",
            "advertisement_small",
            "advertisement_medium",
            "advertisement_group",
        ]

    @staticmethod
    def advertisement():
        return [
            "story_window",
            "advertisement_small",
            "advertisement_medium",
            "advertisement_group",
        ]
