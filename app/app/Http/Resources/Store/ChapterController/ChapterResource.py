from django.db.models.query import QuerySet
from django.http import JsonResponse

from app.Domain.Chapter.Models.Chapter import Chapter
from app.Domain.Chapter.Services.ChapterService import ChapterService
from app.Domain.Customer.Models.Customer import Customer
from app.Domain.File.Services.FileableService import FileableService
from app.Enums.CollectionEnum import CollectionNameEnum


class ChapterResource(JsonResponse):
    def __init__(self, chapter: Chapter, customer: Customer, isEmpty: bool = False, status=200, safe=False, json_dumps_params=None, **kwargs):
        fileableService = FileableService()
        chapterService = ChapterService()
        chapterText = chapter.text
        chapter: QuerySet[Chapter] = chapterService.findBy({"id": chapter.id})
        chapter = chapter.prefetch_related("fileable__file", "story__chapter_set")[0]

        if isEmpty:
            chapterText = None
            chapterList = []
            images = []
            audio = []
            reaction = {
                "like": 0,
                "dislike": 0,
                "is_liked": False,
                "is_disliked": False,
            }
        else:
            fileables = chapter.fileable.all()
            chapterList = chapterService.getChapteListByStory(chapter.story)
            images = fileableService.transformImagesByCollection(fileables, CollectionNameEnum.STORY_IMAGE, "store")
            audio = fileableService.transformAudioByCollection(fileables, CollectionNameEnum.CHAPTER_AUDIO, "store")
            reaction = chapterService.transformReactionByChapterAndCustomer(chapter, customer)

        self.data = {
            "id": chapter.id,
            "story_name": chapter.story.name,
            "type": chapter.type,
            "text": chapterText,
            "images": images,
            "audio": audio,
            "reaction": reaction,
            "chapter_list": chapterList,
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
