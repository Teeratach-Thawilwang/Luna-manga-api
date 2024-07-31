class CustomerReportSourceEnum:
    STORY = "story"
    CHAPTER = "chapter"
    POST = "post"
    COMMENT = "comment"

    @staticmethod
    def list():
        return [
            "story",
            "chapter",
            "post",
            "comment",
        ]
