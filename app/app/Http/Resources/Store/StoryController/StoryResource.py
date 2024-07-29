from app.Domain.Customer.Models.Customer import Customer
from app.Domain.File.Services.FileableService import FileableService
from app.Domain.Story.Models.Story import Story
from app.Domain.Story.Services.StoryService import StoryService
from app.Enums.CollectionEnum import CollectionNameEnum
from django.http import JsonResponse


class StoryResource(JsonResponse):
    def __init__(self, story: Story, customer: Customer | None, status=200, safe=False, json_dumps_params=None, **kwargs):
        storyService = StoryService()
        self.data = {
            "id": story.id,
            "slug": story.slug,
            "name": story.name,
            "description": story.description,
            "view_count": storyService.getViewCountFromChapter(story),
            "type": story.type,
            "reaction": storyService.transformReactionByStoryAndCustomer(story, customer),
            # "author": storyService.getAuthor(story.customer),
            "author": self.getAuthor(story),
            "images": FileableService().transformImagesByCollection(story.fileable, CollectionNameEnum.STORY_IMAGE, "store"),
            "categories": storyService.transformCategories(story.categories.all()),
            "is_bookmark": storyService.isBookmark(story, customer),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def getAuthor(self, story: Story):
        return {
            "id": 1,
            "display_name": story.author_name,
        }
