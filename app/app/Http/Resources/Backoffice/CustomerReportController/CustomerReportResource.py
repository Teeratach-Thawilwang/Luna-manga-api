from app.Domain.Chapter.Models.Chapter import Chapter
from app.Domain.Comment.Models.Comment import Comment
from app.Domain.Customer.Models.Customer import Customer
from app.Domain.CustomerReport.Models.CustomerReport import CustomerReport
from app.Domain.Post.Models.Post import Post
from app.Domain.Story.Models.Story import Story
from app.Enums.CustomerReportSourceEnum import CustomerReportSourceEnum
from app.Services.LocalTime import localTime
from django.http import JsonResponse


class CustomerReportResource(JsonResponse):
    def __init__(self, customerReport: CustomerReport, status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = {
            "id": customerReport.id,
            "group": customerReport.group,
            "source": customerReport.model_type.model,
            "data": self.transformData(customerReport.model, customerReport.model_type.model),
            "message": customerReport.message,
            "reporter": self.getReport(customerReport.customer),
            "is_accept": customerReport.is_accept,
            "accept_by": self.getAcceptBy(customerReport),
            "created_at": localTime(customerReport.created_at),
            "updated_at": localTime(customerReport.updated_at),
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)

    def transformData(self, model: Story | Chapter, type: CustomerReportSourceEnum):
        match type:
            case CustomerReportSourceEnum.STORY:
                return self.getStoryDetail(model)
            case CustomerReportSourceEnum.CHAPTER:
                return self.getChapterDetail(model)
            case CustomerReportSourceEnum.POST:
                return self.getPostDetail(model)
            case CustomerReportSourceEnum.COMMENT:
                return self.getCommentDetail(model)

    def getReport(self, customer: Customer) -> dict[str]:
        return {
            "id": customer.id,
            "email": customer.email,
            "nick_name": customer.nick_name,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "created_at": customer.created_at,
            "updated_at": customer.updated_at,
        }

    def getAcceptBy(self, customerReport: CustomerReport):
        if customerReport.accept_by == None:
            return ""

        user = customerReport.accept_by
        return f"{user.first_name} {user.last_name} (id={user.id})"

    def getStoryDetail(self, story: Story) -> dict[str]:
        return {
            "id": story.id,
            "slug": story.slug,
            "name": story.name,
            "type": story.type,
            "created_at": story.created_at,
            "updated_at": story.updated_at,
        }

    def getChapterDetail(self, chapter: Chapter) -> dict[str]:
        return {
            "id": chapter.id,
            "name": chapter.name,
            "chapter_number": chapter.chapter_number,
            "story": self.getStoryDetail(chapter.story),
            "created_at": chapter.created_at,
            "updated_at": chapter.updated_at,
        }

    def getPostDetail(self, post: Post) -> dict[str]:
        return {
            "id": post.id,
            "commenter": self.getCustomerDetail(post.customer),
            "message": post.text,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
        }

    def getCommentDetail(self, comment: Comment) -> dict[str]:
        return {
            "id": comment.id,
            "chapter": self.getChapterDetail(comment.chapter),
            "commenter": self.getCustomerDetail(comment.customer),
            "message": comment.text,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
        }

    def getCustomerDetail(self, customer: Customer) -> dict[str]:
        return {
            "id": customer.id,
            "email": customer.email,
            "nick_name": customer.nick_name,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "created_at": customer.created_at,
            "updated_at": customer.updated_at,
        }
