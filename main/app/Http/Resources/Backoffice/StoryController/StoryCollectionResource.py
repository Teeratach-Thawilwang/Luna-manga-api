from app.Domain.Story.Services.StoryService import StoryService
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class StoryCollectionResource(JsonResponse):
    def __init__(self, data, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = data
        super().__init__(self.toArray(), status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def toArray(self):
        data = []
        for story in self.data["data"]:
            data.append(
                {
                    "id": story.id,
                    "name": story.name,
                    "type": story.type,
                    "status": story.status,
                    "author_name": StoryService().getAuthorName(story),
                    "total_chapter": story.chapter_set.count(),
                    "rating_score": StoryService().getRating(story),
                    "created_at": localTime(story.created_at),
                    "updated_at": localTime(story.updated_at),
                }
            )
        self.data["data"] = data
        return self.data
