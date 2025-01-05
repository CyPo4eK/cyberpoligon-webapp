from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('admin/', views.admin_page, name='admin_pages')
]
