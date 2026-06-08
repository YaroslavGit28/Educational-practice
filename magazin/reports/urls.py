from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_index, name='index'),
    path('export/', views.export_sales_excel, name='export_excel'),
]
