from django.urls import path

from .views import SalesReportExportView, SalesReportView

app_name = "reports"

urlpatterns = [
    path("sales/", SalesReportView.as_view(), name="sales"),
    path("sales/export/", SalesReportExportView.as_view(), name="sales_export"),
]
