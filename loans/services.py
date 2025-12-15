import requests
import os
from decimal import Decimal

class EligibilityService:
    BASE_URL = os.environ.get('API_BASE_URL', 'http://127.0.0.1:8000')

    def check_eligibility(self, data):
        national_id = data['national_id']
        loan_amount = Decimal(data['loan_amount'])
        term_months = int(data['term_months'])
        
        # 1. Salary Verification
        try:
            salary_response = requests.get(f"{self.BASE_URL}/api/mocks/salary/{national_id}/", timeout=5)
            if salary_response.status_code != 200:
                return {"eligible": False, "reason": "Salary verification service unavailable or failed."}
            salary_data = salary_response.json()
            monthly_salary = Decimal(salary_data['monthly_salary'])
        except requests.RequestException:
             return {"eligible": False, "reason": "Salary verification service connection error."}

        # 2. Credit Bureau Check
        try:
            credit_response = requests.get(f"{self.BASE_URL}/api/mocks/credit/{national_id}/", timeout=5)
            if credit_response.status_code != 200:
                return {"eligible": False, "reason": "Credit bureau service unavailable or failed."}
            credit_data = credit_response.json()
            credit_score = credit_data['credit_score']
            active_defaults = credit_data['active_defaults']
            active_loans = credit_data['active_loans']
        except requests.RequestException:
            return {"eligible": False, "reason": "Credit bureau service connection error."}

        # 3. Apply Rules
        # Rule 1: Monthly salary must be at least 3x the monthly repayment
        monthly_repayment = loan_amount / term_months
        if monthly_salary < (monthly_repayment * 3):
            return {
                "eligible": False, 
                "reason": f"Insufficient salary. Monthly salary ({monthly_salary}) must be at least 3x monthly repayment ({monthly_repayment:.2f})."
            }

        # Rule 2: Credit score must be 600 or above
        if credit_score < 600:
             return {"eligible": False, "reason": f"Credit score too low. Score: {credit_score}, Required: 600."}
             
        # Rule 3: No active defaults
        if active_defaults:
            return {"eligible": False, "reason": "Applicant has active defaults."}
            
        # Rule 4: Maximum 3 active loans
        if active_loans > 3:
            return {"eligible": False, "reason": f"Too many active loans. Current: {active_loans}, Max: 3."}

        # If all checks pass
        return {
            "eligible": True,
            "message": "Loan approved.",
            "details": {
                "approved_amount": loan_amount,
                "term_months": term_months,
                "monthly_repayment": round(monthly_repayment, 2)
            }
        }
