class StatusEnum:
    ACTIVE = "active"
    INACTIVE = "inactive"

    @staticmethod
    def list():
        return ["active", "inactive"]


class UserStatusEnum(StatusEnum):
    pass


class CustomerStatusEnum(StatusEnum):
    pass


class CustomerGroupStatusEnum(StatusEnum):
    pass


class CategoryStatusEnum(StatusEnum):
    pass


class ChapterStatusEnum(StatusEnum):
    pass


class BannerStatusEnum(StatusEnum):
    pass


class WidgetStatusEnum(StatusEnum):
    pass


class StoryStatusEnum:
    ONGOING = "ongoing"
    INACTIVE = "inactive"
    FINISHED = "finished"

    @staticmethod
    def list():
        return ["ongoing", "inactive", "finished"]
