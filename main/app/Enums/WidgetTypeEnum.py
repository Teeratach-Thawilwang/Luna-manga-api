class WidgetTypeEnum:
    STORY_LIST = "story_list"
    STORY_WINDOW = "story_window"
    STORY_GROUP = "story_group"
    CHAPTER_GROUP = "chapter_group"
    ADVERTISEMENT_SMALL = "advertisement_small"
    ADVERTISEMENT_MEDIUM = "advertisement_medium"
    ADVERTISEMENT_GROUP = "advertisement_group"

    @staticmethod
    def list():
        return [
            "story_list",
            "story_window",
            "story_group",
            "chapter_group",
            "advertisement_small",
            "advertisement_medium",
            "advertisement_group",
        ]
