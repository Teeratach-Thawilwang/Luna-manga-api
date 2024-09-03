from django.db.models import Sum
from django.http import JsonResponse

from app.Domain.File.Services.FileableService import FileableService
from app.Domain.Story.Models.Story import Story
from app.Domain.Story.Services.StoryService import StoryService
from app.Enums.CollectionEnum import CollectionNameEnum


class StorySearchCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        storyService = StoryService()
        fileableService = FileableService()
        stories = self.data["data"].prefetch_related("storyreaction_set", "chapter_set", "fileable__file").all()
        stories = stories.annotate(sum_view_count=Sum("chapter__view_count"))
        stories = stories.annotate(like__sum=Sum("storyreaction__like"))

        for story in stories:
            data.append(
                {
                    "id": story.id,
                    "slug": story.slug,
                    "name": story.name,
                    "type": story.type,
                    "author": self.getAuthor(story),
                    "rating_score": storyService.getRating(story),
                    "view_count": story.sum_view_count,
                    "images": fileableService.transformImagesByCollection(story.fileable.all(), CollectionNameEnum.STORY_IMAGE, "store"),
                    # "categories": storyService.transformCategories(story.categories.all()),
                }
            )
        self.data["data"] = data
        return self.data

    def getAuthor(self, story: Story):
        return {
            "id": 1,
            "display_name": story.author_name,
        }
