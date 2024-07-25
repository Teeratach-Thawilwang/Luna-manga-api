from app.Http.Controllers.Store.BookmarkController.BookmarkController import BookmarkController
from app.Http.Controllers.Store.CategoryController.CategoryController import CategoryController
from app.Http.Controllers.Store.CategoryStoryController.CategoryStoryController import CategoryStoryController
from app.Http.Controllers.Store.ChapterController.ChapterController import ChapterController
from app.Http.Controllers.Store.ChapterReactionController.ChapterReactionController import ChapterReactionController
from app.Http.Controllers.Store.CommentController.CommentController import CommentController
from app.Http.Controllers.Store.CommentReactionController.CommentReactionController import CommentReactionController
from app.Http.Controllers.Store.CustomerProfileController.CustomerProfileController import CustomerProfileController
from app.Http.Controllers.Store.CustomerReportController.CustomerReportController import CustomerReportController
from app.Http.Controllers.Store.FileController.FileController import FileController
from app.Http.Controllers.Store.ForgotPasswordController.ForgotPasswordController import ForgotPasswordController
from app.Http.Controllers.Store.PostController.PostController import PostController
from app.Http.Controllers.Store.PostReactionController.PostReactionController import PostReactionController
from app.Http.Controllers.Store.ProfileController.ProfileController import ProfileController
from app.Http.Controllers.Store.RegisterController.RegisterController import RegisterController
from app.Http.Controllers.Store.SessionController.SessionController import SessionController
from app.Http.Controllers.Store.StoryChapterController.StoryChapterController import StoryChapterController
from app.Http.Controllers.Store.StoryController.StoryController import StoryController
from app.Http.Controllers.Store.StoryReactionController.StoryReactionController import StoryReactionController
from app.Http.Controllers.Store.WidgetController.WidgetController import WidgetController
from app.Services.Helpers import only
from django.urls import path

urlpatterns = [
    # RegisterController
    path("register", RegisterController.as_view({"post": "register"})),
    path("confirm-register-email", RegisterController.as_view({"post": "confirmEmail"})),
    # ForgotPasswordController
    path("forgot-password", ForgotPasswordController.as_view({"post": "forgotPassword"})),
    path("reset-password", ForgotPasswordController.as_view({"post": "resetPassword"})),
    # SessionController
    path("token", SessionController.as_view({"post": "token"})),
    path("session", SessionController.as_view({"post": "session", "delete": "revoke"})),
    path("social-session", SessionController.as_view({"post": "social_session"})),
    path("session-refresh", SessionController.as_view({"post": "refresh"})),
    # CustomerProfileController
    path("customer-profile", CustomerProfileController.as_view(only(["show", "update"]))),
    # ProfileController
    path("profile/<int:id>", ProfileController.as_view(only(["show"]))),
    # WidgetController
    path("widgets", WidgetController.as_view(only(["index"]))),
    path("widgets/<int:id>/banners", WidgetController.as_view({"get": "widgetBanners"})),
    path("widgets-on-page", WidgetController.as_view({"get": "widgetOnPage"})),
    # FileController
    path("file", FileController.as_view(only(["store"]))),
    path("file/<str:uuid>", FileController.as_view(only(["show"]))),
    # PostController
    path("posts", PostController.as_view(only(["index", "store"]))),
    path("posts/<int:id>", PostController.as_view(only(["update", "destroy"]))),
    # PostReactionController
    path("post-reaction/<int:id>", PostReactionController.as_view(only(["update"]))),
    # CommentController
    path("comments", CommentController.as_view(only(["index", "store"]))),
    path("comments/<int:id>", CommentController.as_view(only(["update", "destroy"]))),
    # CommentReactionController
    path("comment-reaction/<int:id>", CommentReactionController.as_view(only(["update"]))),
    # ChapterController
    path("story/<str:slug>/chapter/<int:number>", ChapterController.as_view(only(["show"]))),
    # ChapterReactionController
    path("chapter-reaction/<int:id>", ChapterReactionController.as_view(only(["update"]))),
    # StoryController
    path("story-search", StoryController.as_view({"get": "storySearch"})),
    path("story/<str:slug>", StoryController.as_view(only(["show"]))),
    # StoryReactionController
    path("story-reaction/<int:id>", StoryReactionController.as_view(only(["update"]))),
    # StoryChapterController
    path("story-chapters/<str:slug>", StoryChapterController.as_view(only(["index"]))),
    # BookmarkController
    path("bookmarks", BookmarkController.as_view(only(["index", "store", "destroy"]))),
    # CategoryController
    path("categories", CategoryController.as_view(only(["index"]))),
    # CategoryStoryController
    path("category-stories/<int:id>", CategoryStoryController.as_view(only(["index"]))),
    # BookmarkController
    path("customer-report", CustomerReportController.as_view(only(["store"]))),
]
