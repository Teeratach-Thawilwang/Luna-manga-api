from django.core.management.base import BaseCommand

from app.Domain.Story.Models.Story import Story
from app.Domain.Story.Services.StoryService import StoryService
from app.Domain.User.Models.User import User
from app.Enums.BannerTypeEnum import BannerTypeEnum

"""
To run command
shell  run => python manage.py UpdateBannerStory <StartIndex> <StopIndex>
docker run => docker-compose exec app python manage.py UpdateBannerStory <StartIndex> <StopIndex>
"""


class Command(BaseCommand):
    help = f"Update widget type={BannerTypeEnum.CHAPTER}."

    def add_arguments(self, parser):
        parser.add_argument("StartIndex", type=int, help="Index to start execution. Default = 0.", nargs="?", default=0)
        parser.add_argument("StopIndex", type=int, help="Index to stop execution. Default = None", nargs="?", default=None)

    def handle(self, *args, **kwargs):
        startIndex = kwargs["StartIndex"]
        stopIndex = kwargs["StopIndex"]

        user = User.objects.get(pk=1)
        stories = Story.objects.values("id", "name", "status", "slug").all()[startIndex:stopIndex]
        for story in stories:
            storyMap = StoryMock(
                id=story["id"],
                name=story["name"],
                status=story["status"],
                slug=story["slug"],
            )
            StoryService().updateOrCreateBannerFromStory(storyMap, user)

        print(f"Update banner type={BannerTypeEnum.STORY} successfully.")


class StoryMock:
    def __init__(self, id, name, status, slug):
        self.id = id
        self.name = name
        self.status = status
        self.slug = slug
