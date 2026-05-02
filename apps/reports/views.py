from collections import defaultdict
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView
from openpyxl import Workbook

from apps.orders.models import OrderItem


class AdminOnlyMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == "admin" or self.request.user.is_superuser


class SalesReportView(AdminOnlyMixin, TemplateView):
    template_name = "reports/sales.html"

    @staticmethod
    def build_sales_rows():
        since = timezone.now() - timedelta(days=30)
        rows = defaultdict(lambda: {"orders": 0, "amount": 0})
        for item in OrderItem.objects.filter(order__created_at__gte=since).select_related("order"):
            key = item.order.created_at.date().isoformat()
            rows[key]["orders"] += 1
            rows[key]["amount"] += float(item.subtotal)
        return dict(rows)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = self.build_sales_rows()
        context["sales_rows"] = dict(rows)
        context["top_products"] = (
            OrderItem.objects.values("product__name").order_by("product__name")[:10]
        )
        return context


class SalesReportExportView(AdminOnlyMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Sales"
        sheet.append(["Date", "Orders", "Amount"])
        for row in SalesReportView.build_sales_rows().items():
            date, payload = row
            sheet.append([date, payload["orders"], payload["amount"]])
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="sales_report.xlsx"'
        workbook.save(response)
        return response
