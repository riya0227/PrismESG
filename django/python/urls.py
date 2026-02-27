from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analytics/', views.analytics, name='analytics'),
    path('upload/', views.upload_report, name='upload_report'),
    path('reports/', views.report_list, name='report_list'),
    path('delete/<int:report_id>/', views.delete_report, name='delete_report'),
    path('edit/<int:report_id>/', views.edit_report, name='edit_report'),
    path("report-detail/", views.report_detail, name="report_detail"),
    path("gap-analysis/", views.gap_analysis, name="gap_analysis"),

]
