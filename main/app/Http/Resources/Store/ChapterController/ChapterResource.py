from app.Domain.Chapter.Models.Chapter import Chapter
from app.Domain.Chapter.Services.ChapterService import ChapterService
from app.Domain.Customer.Models.Customer import Customer
from app.Domain.File.Services.FileableService import FileableService
from app.Enums.CollectionEnum import CollectionNameEnum
from django.http import JsonResponse


class ChapterResource(JsonResponse):
    def __init__(self, chapter: Chapter, customer: Customer, status=200, safe=False, json_dumps_params=None, **kwargs):
        fileableService = FileableService()
        chapterService = ChapterService()
        self.data = {
            "id": chapter.id,
            "story_name": chapter.story.name,
            "type": chapter.type,
            "text": chapter.text,
            "images": fileableService.transformImagesByCollection(chapter.fileable, CollectionNameEnum.STORY_IMAGE, "store"),
            "audio": fileableService.transformAudioByCollection(chapter.fileable, CollectionNameEnum.CHAPTER_AUDIO, "store"),
            "reaction": chapterService.transformReactionByChapterAndCustomer(chapter, customer),
            "chapter_list": chapterService.getChapteListByStory(chapter.story),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
