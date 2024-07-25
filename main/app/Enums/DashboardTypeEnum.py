class DashboardTypeEnum:
    # ORDER = "Order"
    VISIT = "Visit"
    MANGA_VIEW = "Manga View"
    NOVEL_VIEW = "Novel View"
    NEW_CUSTOMER = "New Customer"
    STORY_REPORT = "Story Report"
    CHAPTER_REPORT = "Chapter Report"
    POST_REPORT = "Post Report"
    COMMENT_REPORT = "Comment Report"

    @staticmethod
    def list():
        return [
            # "Order",
            "Visit",
            "Manga View",
            "Novel View",
            "New Customer",
            "Story Report",
            "Chapter Report",
            "Post Report",
            "Comment Report",
        ]
