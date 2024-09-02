from django.db.models import Sum
from django.http import JsonResponse

from app.Domain.File.Services.FileableService import FileableService
from app.Domain.Story.Services.StoryService import StoryService
from app.Enums.CollectionEnum import CollectionNameEnum


class CategoryStoryCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        storyService = StoryService()
        fileableService = FileableService()
        stories = self.data["data"].prefetch_related("storyreaction_set", "chapter_set", "fileable__file").all()
        stories = stories.annotate(sum_view_count=Sum("chapter__view_count"))

        for story in stories:
            data.append(
                {
                    "id": story.id,
                    "slug": story.slug,
                    "name": story.name,
                    "type": story.type,
                    "author": story.author_name,
                    "rating_score": storyService.getRating(story),
                    "view_count": story.sum_view_count,
                    "images": fileableService.transformImagesByCollection(story.fileable.all(), CollectionNameEnum.STORY_IMAGE, "store"),
                }
            )
        self.data["data"] = data
        return self.data
