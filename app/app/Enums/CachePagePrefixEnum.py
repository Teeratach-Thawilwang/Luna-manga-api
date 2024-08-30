class CachePagePrefixEnum:
    PRESIGNED_URL = "presigned_url"
    STORE_WIDGET_INDEX = "store_widget_index"
    STORE_WIDGET_ON_PAGE = "store_widget_on_page"
    STORE_WIDGET_BANNER = "store_widget_banner"
    STORE_STORY_SEARCH = "store_story_search"
    STORE_STORY_SHOW = "store_story_show"
    STORE_STORY_CHAPTER_INDEX = "store_story_chapter_index"
    STORE_CHAPTER_SHOW = "store_chapter_show"
    STORE_CATEGORY_INDEX = "store_category_index"
    STORE_CATEGORY_STORY_INDEX = "store_category_story_index"

    @staticmethod
    def list():
        return [
            "presigned_url",
            "store_widget_index",
            "store_widget_on_page",
            "store_widget_banner",
            "store_story_search",
            "store_story_show",
            "store_story_chapter_index",
            "store_chapter_show",
            "store_category_index",
            "store_category_story_index",
        ]
