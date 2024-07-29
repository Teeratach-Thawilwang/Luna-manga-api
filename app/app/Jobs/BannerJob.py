from app.Domain.Banner.Models.Banner import Banner
from app.Domain.Banner.Services.BannerService import BannerService


class BannerJob:
    def syncFileable(banner: Banner, storyId: int, chapterId: int, imageIds: list[int]):
        BannerService().syncBannerFileable(banner.id, banner.type, storyId, chapterId, imageIds)
