from django.urls import path
from .views import LoanEligibilityView

urlpatterns = [
    path('eligibility/', LoanEligibilityView.as_view(), name='loan-eligibility'),
]
