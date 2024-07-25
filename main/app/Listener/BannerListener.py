from app.Domain.Banner.Models.Banner import Banner
from app.Enums.QueueGroupEnum import QueueGroupEnum
from django_q.tasks import async_task


class BannerListener:
    def syncFileable(self, banner: Banner, storyId: int, chapterId: int, imageIds: list[int]):
        options = {
            "task_name": f"sync banner fileable {banner.id}",
            "group": QueueGroupEnum.SYNC_BANNER_FILEABLE,
        }
        async_task("app.Jobs.BannerJob.BannerJob.syncFileable", banner, storyId, chapterId, imageIds, q_options=options)
