from django.urls import path
from . import views

urlpatterns = [
    path('salary/<str:national_id>/', views.salary_verification, name='mock-salary'),
    path('credit/<str:national_id>/', views.credit_check, name='mock-credit'),
]
