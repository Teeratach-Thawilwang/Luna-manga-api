from django.db.models import Sum
from django.http import JsonResponse

from app.Domain.Customer.Models.Customer import Customer
from app.Domain.File.Services.FileableService import FileableService
from app.Domain.Story.Models.Story import Story
from app.Domain.Story.Services.StoryService import StoryService
from app.Enums.CollectionEnum import CollectionNameEnum


class StoryResource(JsonResponse):
    def __init__(self, story: Story, customer: Customer | None, status=200, safe=False, json_dumps_params=None, **kwargs):
        storyService = StoryService()
        story = story.annotate(sum_view_count=Sum("chapter__view_count")).all()[0]

        self.data = {
            "id": story.id,
            "slug": story.slug,
            "name": story.name,
            "description": story.description,
            "view_count": story.sum_view_count,
            "type": story.type,
            "reaction": storyService.transformReactionByStoryAndCustomer(story, customer),
            "author": self.getAuthor(story),
            "images": FileableService().transformImagesByCollection(story.fileable.all(), CollectionNameEnum.STORY_IMAGE, "store"),
            # "categories": storyService.transformCategories(story.categories.all()),
            "is_bookmark": storyService.isBookmark(story, customer),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def getAuthor(self, story: Story):
        return {
            "id": 1,
            "display_name": story.author_name,
        }
