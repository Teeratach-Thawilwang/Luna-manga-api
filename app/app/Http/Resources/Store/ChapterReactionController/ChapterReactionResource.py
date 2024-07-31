from app.Domain.Chapter.Models.Chapter import Chapter
from app.Domain.Chapter.Services.ChapterService import ChapterService
from app.Domain.Customer.Models.Customer import Customer
from django.http import JsonResponse


class ChapterReactionResource(JsonResponse):
    def __init__(self, post: Chapter, customer: Customer | None, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = ChapterService().transformReactionByChapterAndCustomer(post, customer)
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
