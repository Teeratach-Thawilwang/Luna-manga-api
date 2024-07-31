from app.Domain.File.Services.FileableService import FileableService
from app.Domain.Story.Models.Story import Story
from app.Enums.CollectionEnum import CollectionNameEnum
from app.Http.Resources.Backoffice.CategoryController.CategoryCollectionResource import CategoryCollectionResource
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class StoryResource(JsonResponse):
    def __init__(self, story: Story, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = {
            "id": story.id,
            "name": story.name,
            "slug": story.slug,
            "description": story.description,
            "type": story.type,
            "status": story.status,
            "categories": CategoryCollectionResource({"data": story.categories.all()}).data["data"],
            "cover_image": FileableService().transformImagesByCollection(story.fileable, CollectionNameEnum.STORY_IMAGE),
            "created_at": localTime(story.created_at),
            "updated_at": localTime(story.updated_at),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
