from app.Domain.Comment.Models.Comment import Comment
from factory import Faker
from factory.django import DjangoModelFactory


class CommentFactory(DjangoModelFactory):
    customer_id = 1
    chapter_id = 1
    text = Faker("text", max_nb_chars=100)

    class Meta:
        model = Comment
