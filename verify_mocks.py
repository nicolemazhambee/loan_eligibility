import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

subjects = [
    "12345678", "12345679", "12345680", "12345681", "12345682",
    "12345683", "12345684", "12345685", "12345686", "12345687"
]

def check(id):
    print(f"\nChecking ID: {id}")
    try:
        sal = requests.get(f"{BASE_URL}/api/mocks/salary/{id}/").json()
        cred = requests.get(f"{BASE_URL}/api/mocks/credit/{id}/").json()
        print(f"Salary: {sal.get('monthly_salary')} {sal.get('currency')}")
        print(f"Credit: {cred.get('credit_score')}, Loans: {cred.get('active_loans')}, Defaults: {cred.get('active_defaults')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    for s in subjects:
        check(s)
