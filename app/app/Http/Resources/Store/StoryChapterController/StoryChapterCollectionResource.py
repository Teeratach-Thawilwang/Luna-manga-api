from django.db.models import Sum
from django.http import JsonResponse

from app.Domain.Chapter.Models import Chapter
from app.Domain.Chapter.Services.ChapterService import ChapterService
from app.Domain.File.Services.FileableService import FileableService
from app.Enums.CollectionEnum import CollectionNameEnum
from app.Services.LocalTime import localTime


class StoryChapterCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        fileableService = FileableService()
        chapters = self.data["data"].prefetch_related("chapterreaction_set").all()
        chapters = chapters.annotate(like__sum=Sum("chapterreaction__like"))
        fileable = None

        for chapter in chapters:
            # In case of every chapter use the same chapter-cover-image
            if fileable == None:
                fileable = chapter.fileable.select_related("file").filter(file__collection_name=CollectionNameEnum.CHAPTER_COVER_IMAGE).first()
                print("do herer")
            data.append(
                {
                    "id": chapter.id,
                    "name": chapter.name,
                    "chapter_number": chapter.chapter_number,
                    "score": self.getScore(chapter),
                    "view_count": chapter.view_count,
                    "cover_images": fileableService.transformImagesByCollection([fileable], CollectionNameEnum.CHAPTER_COVER_IMAGE, "store"),
                    "release_date": localTime(chapter.created_at),
                }
            )
        self.data["data"] = data
        return self.data

    def getScore(self, chapter: Chapter) -> int:
        totalReaction = chapter.chapterreaction_set.count()
        if totalReaction == 0:
            return 0

        like = chapter.like__sum
        like = 0 if like == None else like
        return float("{:.2f}".format(like / totalReaction))
