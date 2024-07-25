from django.http import JsonResponse


class DashboardResource(JsonResponse):
    def __init__(self, items: dict[str, list[str]], status=200, safe=False, json_dumps_params=None, **kwargs):
        self.data = {
            "data": items,
        }
        super().__init__(self.data, status=status, safe=safe, json_dumps_params=json_dumps_params, **kwargs)
