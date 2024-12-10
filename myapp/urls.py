from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='signup'),
    path('home/', views.home, name='home'),
    path('sales/', views.sales, name='sales'),
    path('visual_report/', views.visual_report, name='visual_report'),
    path('sales_form/', views.sales_form, name='sales_form'),
    path('sales_view/', views.sales_view, name='sales_view'),

    path('single_day_report/', views.single_day_report, name='single_day_report'),
    path('month_report/', views.month_report, name='month_report'),
    path('add_expenses/', views.add_expense, name='add_expense'),
    path('view_expenses/', views.view_expenses, name='view_expenses'),
    path('business_performance/', views.business_performance, name='business_performance'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('update_product/<int:id>/', views.update_product, name='update_product'),
    path('logout/', views.custom_logout, name='logout'),
]
