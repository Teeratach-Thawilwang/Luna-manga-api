from app.Http.Controllers.Backoffice.BannerController.BannerController import BannerController
from app.Http.Controllers.Backoffice.CategoryController.CategoryController import CategoryController
from app.Http.Controllers.Backoffice.ChapterController.ChapterController import ChapterController
from app.Http.Controllers.Backoffice.CustomerController.CustomerController import CustomerController
from app.Http.Controllers.Backoffice.CustomerGroupController.CustomerGroupController import CustomerGroupController
from app.Http.Controllers.Backoffice.CustomerReportController.CustomerReportController import CustomerReportController
from app.Http.Controllers.Backoffice.DashboardController.DashboardController import DashboardController
from app.Http.Controllers.Backoffice.FileController.FileController import FileController
from app.Http.Controllers.Backoffice.OAuthClientController.OAuthClientController import OAuthClientController
from app.Http.Controllers.Backoffice.PermissionController.PermissionController import PermissionController
from app.Http.Controllers.Backoffice.RoleController.RoleController import RoleController
from app.Http.Controllers.Backoffice.SessionController.SessionController import SessionController
from app.Http.Controllers.Backoffice.StoryController.StoryController import StoryController
from app.Http.Controllers.Backoffice.UserController.UserController import UserController
from app.Http.Controllers.Backoffice.UserProfileController.UserProfileController import UserProfileController
from app.Http.Controllers.Backoffice.WidgetController.WidgetController import WidgetController
from app.Http.Controllers.Backoffice.WidgetSequenceController.WidgetSequenceController import WidgetSequenceController
from app.Services.Helpers import only
from django.urls import path

urlpatterns = [
    # SessionController
    path("token", SessionController.as_view({"post": "token"})),
    path("session", SessionController.as_view({"post": "session", "delete": "revoke"})),
    path("session-refresh", SessionController.as_view({"post": "refresh"})),
    # UserProfileController
    path("user-profile", UserProfileController.as_view(only(["show"]))),
    path("user-profile/<int:id>", UserProfileController.as_view(only(["update"]))),
    # DashboardController
    path("dashboard", DashboardController.as_view(only(["show"]))),
    # StoryController
    path("stories", StoryController.as_view(only(["index", "store"]))),
    path("stories/<int:id>", StoryController.as_view(only(["show", "update", "destroy"]))),
    # ChapterController
    path("chapters", ChapterController.as_view(only(["index", "store"]))),
    path("chapters/<int:id>", ChapterController.as_view(only(["show", "update", "destroy"]))),
    # CategoryController
    path("categories", CategoryController.as_view(only(["index", "store"]))),
    path("categories/<int:id>", CategoryController.as_view(only(["show", "update", "destroy"]))),
    # CustomerController
    path("customers", CustomerController.as_view(only(["index"]))),
    path("customers/<int:id>", CustomerController.as_view(only(["show", "update"]))),
    # CustomerGroupController
    path("customer-groups", CustomerGroupController.as_view(only(["index", "store"]))),
    path("customer-groups/<int:id>", CustomerGroupController.as_view(only(["show", "update", "destroy"]))),
    # UserController
    path("users", UserController.as_view(only(["index", "store"]))),
    path("users/<int:id>", UserController.as_view(only(["show", "update", "destroy"]))),
    # OAuthClientController
    path("oauth-clients", OAuthClientController.as_view(only(["index", "store"]))),
    path("oauth-clients/<int:id>", OAuthClientController.as_view(only(["show", "update", "destroy"]))),
    # RoleController
    path("roles", RoleController.as_view(only(["index", "store"]))),
    path("roles/<int:id>", RoleController.as_view(only(["show", "update", "destroy"]))),
    # PermissionController
    path("permissions", PermissionController.as_view(only(["index"]))),
    # FileCOntroller
    path("file", FileController.as_view(only(["index", "store"]))),
    path("file/<str:uuid>", FileController.as_view(only(["show", "destroy"]))),
    path("file/test/", FileController.as_view({"get": "test"})),
    # BannerController
    path("banners", BannerController.as_view(only(["index", "store"]))),
    path("banners/<int:id>", BannerController.as_view(only(["show", "update", "destroy"]))),
    # WidgetController
    path("widgets", WidgetController.as_view(only(["index", "store"]))),
    path("widgets/<int:id>", WidgetController.as_view(only(["show", "update", "destroy"]))),
    # WidgetSequenceController
    path("widget-sequence", WidgetSequenceController.as_view(only(["index", "update"]))),
    # CustomerReportController
    path("customer-reports", CustomerReportController.as_view(only(["index", "update"]))),
    path("customer-reports/<int:id>", CustomerReportController.as_view(only(["show", "update", "destroy"]))),
]
