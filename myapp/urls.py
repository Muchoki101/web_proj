from django.urls import path
from .  import views

urlpatterns=[

    path('',views.login_view,name='login'),
    path('register/',views.signup_view,name='signup'),
    path('home/',views.home,name='home'),
    path('sales/',views.sales,name='sales'),




]