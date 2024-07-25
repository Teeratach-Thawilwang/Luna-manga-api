from app.Domain.Post.Models.Post import Post
from factory import Faker
from factory.django import DjangoModelFactory


class PostFactory(DjangoModelFactory):
    customer_id = 1
    text = Faker("text", max_nb_chars=100)

    class Meta:
        model = Post
