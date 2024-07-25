from app.Domain.Chapter.Services.ChapterService import ChapterService
from app.Domain.File.Services.FileableService import FileableService
from app.Enums.CollectionEnum import CollectionNameEnum
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class StoryChapterCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        for chapter in self.data["data"]:
            data.append(
                {
                    "id": chapter.id,
                    "name": chapter.name,
                    "chapter_number": chapter.chapter_number,
                    "score": ChapterService().getScore(chapter),
                    "view_count": chapter.view_count,
                    "cover_images": FileableService().transformImagesByCollection(chapter.fileable, CollectionNameEnum.CHAPTER_COVER_IMAGE, "store"),
                    "release_date": localTime(chapter.created_at),
                }
            )
        self.data["data"] = data
        return self.data
