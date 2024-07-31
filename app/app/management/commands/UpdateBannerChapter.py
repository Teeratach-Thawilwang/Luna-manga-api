from django.core.management.base import BaseCommand

from app.Domain.Chapter.Models.Chapter import Chapter
from app.Domain.Chapter.Services.ChapterService import ChapterService
from app.Domain.User.Models.User import User
from app.Enums.BannerTypeEnum import BannerTypeEnum

"""
To run command
shell  run => python manage.py UpdateBannerChapter <StartIndex> <StopIndex>
docker run => docker-compose exec app python manage.py UpdateBannerChapter <StartIndex> <StopIndex>
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
        chapters = Chapter.objects.select_related("story").values("id", "name", "status", "chapter_number", "story__name", "story__slug").all()[startIndex:stopIndex]
        for chapter in chapters:
            chapterMap = ChapterMock(
                id=chapter["id"],
                name=chapter["name"],
                status=chapter["status"],
                chapterNumber=chapter["chapter_number"],
                story=StoryMock(name=chapter["story__name"], slug=chapter["story__slug"]),
            )
            ChapterService().updateOrCreateBannerFromChapter(chapterMap, user)

        print(f"Update banner type={BannerTypeEnum.CHAPTER} successfully.")


class StoryMock:
    def __init__(self, name, slug):
        self.name = name
        self.slug = slug


class ChapterMock:
    def __init__(self, id, name, status, chapterNumber, story):
        self.id = id
        self.name = name
        self.status = status
        self.chapter_number = chapterNumber
        self.story = story
