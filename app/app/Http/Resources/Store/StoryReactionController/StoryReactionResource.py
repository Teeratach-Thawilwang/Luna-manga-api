from app.Domain.Customer.Models.Customer import Customer
from app.Domain.Story.Models.Story import Story
from app.Domain.Story.Services.StoryService import StoryService
from django.http import JsonResponse


class StoryReactionResource(JsonResponse):
    def __init__(self, story: Story, customer: Customer | None, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = StoryService().transformReactionByStoryAndCustomer(story, customer)
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
