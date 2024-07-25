from app.Domain.Chapter.Models.Chapter import Chapter
from app.Domain.Chapter.Services.ChapterService import ChapterService
from app.Domain.File.Services.FileableService import FileableService
from app.Enums.CollectionEnum import CollectionNameEnum
from app.Http.Resources.Backoffice.StoryController.StoryCollectionResource import StoryCollectionResource
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class ChapterResource(JsonResponse):
    def __init__(self, chapter: Chapter, status=200, safe=False, json_dumps_params=None, **kwargs):
        fileableService = FileableService()
        self.data = {
            "id": chapter.id,
            "story": StoryCollectionResource({"data": [chapter.story]}).data["data"][0],
            "name": chapter.name,
            "chapter_number": chapter.chapter_number,
            "type": chapter.type,
            "status": chapter.status,
            "cover_image": fileableService.transformImagesByCollection(chapter.fileable, CollectionNameEnum.CHAPTER_COVER_IMAGE),
            "text": chapter.text,
            "images": fileableService.transformImagesByCollection(chapter.fileable, CollectionNameEnum.STORY_IMAGE),
            "audio": fileableService.transformAudioByCollection(chapter.fileable, CollectionNameEnum.CHAPTER_AUDIO),
            "score": ChapterService().getScore(chapter),
            "view_count": chapter.view_count,
            "created_at": localTime(chapter.created_at),
            "updated_at": localTime(chapter.updated_at),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
