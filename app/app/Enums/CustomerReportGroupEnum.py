class CustomerReportGroupEnum:
    COPYRIGHT_INFRINGEMENT = "copyright_infringement"
    INAPPROPRIATELY_RATED = "inappropriately_rated"
    SEXUAL = "sexual"
    UNRELATED = "unrelated"
    HATE_SPEECH = "hate_speech"
    SPAM = "spam"
    OTHER = "other"

    @staticmethod
    def list():
        return [
            "copyright_infringement",
            "inappropriately_rated",
            "sexual",
            "unrelated",
            "hate_speech",
            "spam",
            "other",
        ]
