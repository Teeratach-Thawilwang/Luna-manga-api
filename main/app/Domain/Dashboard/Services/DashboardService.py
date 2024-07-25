from app.Domain.Authentication.Models.OAuthAccessToken import OAuthAccessToken
from app.Domain.Customer.Models.Customer import Customer
from app.Domain.CustomerReport.Models.CustomerReport import CustomerReport
from app.Enums.CustomerReportSourceEnum import CustomerReportSourceEnum
from app.Enums.DashboardTypeEnum import DashboardTypeEnum
from app.Services.Helpers import getCache, getDatetimeTodayUtc
from django.contrib.contenttypes.models import ContentType


class DashboardService:
    def createDashboardItems(self) -> list[dict[str, list[str]]]:
        data = []
        for type in DashboardTypeEnum.list():
            data.append(self.createItemByType(type))
        return data

    def createItemByType(self, type: DashboardTypeEnum) -> dict[str, list[str]]:
        match type:
            case DashboardTypeEnum.VISIT:
                return self.getVisitItem()
            case DashboardTypeEnum.MANGA_VIEW:
                return self.getMangaViewItem()
            case DashboardTypeEnum.NOVEL_VIEW:
                return self.getNovelViewItem()
            case DashboardTypeEnum.NEW_CUSTOMER:
                return self.getNewCustomerItem()
            case DashboardTypeEnum.STORY_REPORT:
                return self.getReportItem(type, source=CustomerReportSourceEnum.STORY)
            case DashboardTypeEnum.CHAPTER_REPORT:
                return self.getReportItem(type, source=CustomerReportSourceEnum.CHAPTER)
            case DashboardTypeEnum.POST_REPORT:
                return self.getReportItem(type, source=CustomerReportSourceEnum.POST)
            case DashboardTypeEnum.COMMENT_REPORT:
                return self.getReportItem(type, source=CustomerReportSourceEnum.COMMENT)

    def getVisitItem(self) -> dict[str, list[str]]:
        todayUtc = getDatetimeTodayUtc()
        guestTokenCount = OAuthAccessToken.objects.filter(created_at__gte=todayUtc, model_id=None).count()

        customerType = ContentType.objects.get(model="customer")
        customerTokenCount = OAuthAccessToken.objects.filter(created_at__gte=todayUtc, model_id__isnull=False, model_type_id=customerType.id).count()
        return {
            "name": DashboardTypeEnum.VISIT,
            "middle": guestTokenCount + customerTokenCount,
            "left_bottom": [f"{guestTokenCount} Guest"],
            "right_bottom": [f"{customerTokenCount} Customer"],
        }

    def getMangaViewItem(self) -> dict[str, list[str]]:
        viewCount = getCache("manga_view_count", 0)
        return {
            "name": DashboardTypeEnum.MANGA_VIEW,
            "middle": viewCount,
            "left_bottom": [],
            "right_bottom": [],
        }

    def getNovelViewItem(self) -> dict[str, list[str]]:
        viewCount = getCache("novel_view_count", 0)
        return {
            "name": DashboardTypeEnum.NOVEL_VIEW,
            "middle": viewCount,
            "left_bottom": [],
            "right_bottom": [],
        }

    def getNewCustomerItem(self) -> dict[str, list[str]]:
        todayUtc = getDatetimeTodayUtc()
        unConfirmEmailCount = Customer.objects.filter(created_at__gte=todayUtc, email_verified_at=None).count()
        confirmEmailCount = Customer.objects.filter(created_at__gte=todayUtc, email_verified_at__isnull=False).count()
        return {
            "name": DashboardTypeEnum.NEW_CUSTOMER,
            "middle": unConfirmEmailCount + confirmEmailCount,
            "left_bottom": [confirmEmailCount, "Confirm Email"],
            "right_bottom": [unConfirmEmailCount, "Unconfirmed"],
        }

    def getReportItem(self, type: DashboardTypeEnum, source: CustomerReportSourceEnum) -> dict[str, list[str]]:
        todayUtc = getDatetimeTodayUtc()
        modelType = ContentType.objects.get(model=source)
        unAcceptCount = CustomerReport.objects.filter(created_at__gte=todayUtc, model_type_id=modelType.id, accept_by_id__isnull=True).count()
        acceptCount = CustomerReport.objects.filter(created_at__gte=todayUtc, model_type_id=modelType.id, accept_by_id__isnull=False).count()
        return {
            "name": type,
            "middle": unAcceptCount + acceptCount,
            "left_bottom": [acceptCount, "Accepted"],
            "right_bottom": [unAcceptCount, "Unaccepted"],
        }
