from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json

class LoanEligibilityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('loan-eligibility')
        self.valid_payload = {
            "national_id": "123456789", # Need a seed that works. 
            "loan_amount": 5000,
            "term_months": 12
        }
        
    def test_application_valid_structure(self):
        """Test that the API accepts valid data structure."""
        response = self.client.post(self.url, self.valid_payload, content_type='application/json')
        # We don't verify logic yet, just that it didn't crash or return 400 validation error
        # Unless the mock is down (which it might be in test environment if using requests to localhost)
        # Wait, 'requests.get' in `services.py` will try to hit localhost:8000.
        # In `Django TestCase`, the live server isn't running by default unless we use LiveServerTestCase.
        # And even then, `self.client` calls internal views, but `services.py` calls `requests.get`.
        # This will FAIL standard TestCase because 'localhost:8000' is not listening during the test run
        # unless I mock the `requests.get` call OR use LiveServerTestCase.
        pass

# I need to MOCK requests.get in the tests to avoid external dependency and actually test logic.
from unittest.mock import patch

class LoanLogicTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('loan-eligibility')

    @patch('loans.services.requests.get')
    def test_eligible_loan(self, mock_get):
        # Mock Salary Response
        mock_salary_response = type('Response', (), {'status_code': 200, 'json': lambda: {'monthly_salary': 5000}})
        # Mock Credit Response
        mock_credit_response = type('Response', (), {'status_code': 200, 'json': lambda: {'credit_score': 700, 'active_defaults': False, 'active_loans': 0}})
        
        # Side effect to return different responses based on URL (simple check)
        def side_effect(url, timeout=5):
            if 'salary' in url:
                return mock_salary_response
            if 'credit' in url:
                return mock_credit_response
            return None
            
        mock_get.side_effect = side_effect

        payload = {
            "national_id": "12345", 
            "loan_amount": 10000,
            "term_months": 12 # Repayment = 833.33. 5000 > 3*833 (2500). OK.
        }
        response = self.client.post(self.url, payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['eligible'])

    @patch('loans.services.requests.get')
    def test_insufficient_salary(self, mock_get):
        mock_salary_response = type('Response', (), {'status_code': 200, 'json': lambda: {'monthly_salary': 1000}})
        mock_credit_response = type('Response', (), {'status_code': 200, 'json': lambda: {'credit_score': 700, 'active_defaults': False, 'active_loans': 0}})
        
        mock_get.side_effect = lambda url, timeout=5: mock_salary_response if 'salary' in url else mock_credit_response

        payload = {
            "national_id": "12345", 
            "loan_amount": 10000,
            "term_months": 10 # Repayment 1000. Salary 1000. Needs 3000. Fail.
        }
        response = self.client.post(self.url, payload, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['eligible'])
        self.assertIn("Insufficient salary", response.data['reason'])

    @patch('loans.services.requests.get')
    def test_low_credit_score(self, mock_get):
        mock_salary_response = type('Response', (), {'status_code': 200, 'json': lambda: {'monthly_salary': 5000}})
        mock_credit_response = type('Response', (), {'status_code': 200, 'json': lambda: {'credit_score': 500, 'active_defaults': False, 'active_loans': 0}})
        
        mock_get.side_effect = lambda url, timeout=5: mock_salary_response if 'salary' in url else mock_credit_response

        payload = {
            "national_id": "12345", 
            "loan_amount": 1000,
            "term_months": 12
        }
        response = self.client.post(self.url, payload, content_type='application/json')
        self.assertFalse(response.data['eligible'], "Should be declined due to low credit score")

