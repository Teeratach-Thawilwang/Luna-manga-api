from app.Domain.File.Services.FileableService import FileableService
from app.Domain.Story.Models.Story import Story
from app.Domain.Story.Services.StoryService import StoryService
from app.Enums.CollectionEnum import CollectionNameEnum
from django.http import JsonResponse


class BookmarkCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        storyService = StoryService()
        for bookmark in self.data["data"]:
            story: Story = bookmark.story
            data.append(
                {
                    "id": story.id,
                    "slug": story.slug,
                    "name": story.name,
                    "type": story.type,
                    "author": storyService.getAuthor(story.customer),
                    "rating_score": storyService.getRating(story),
                    "view_count": storyService.getViewCountFromChapter(story),
                    "images": FileableService().transformImagesByCollection(story.fileable, CollectionNameEnum.STORY_IMAGE, "store"),
                    "categories": storyService.transformCategories(story.categories.all()),
                }
            )
        self.data["data"] = data
        return self.data
