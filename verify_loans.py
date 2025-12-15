import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/loans/eligibility/"

scenarios = [
    {"id": "12345678", "desc": "Eligible (Standard)", "amount": 5000, "term": 12, "expect": True},
    {"id": "12345679", "desc": "Ineligible (Low Salary)", "amount": 5000, "term": 12, "expect": False},
    {"id": "12345680", "desc": "Ineligible (Low Credit)", "amount": 1000, "term": 12, "expect": False},
    {"id": "12345681", "desc": "Ineligible (Defaults)", "amount": 1000, "term": 12, "expect": False},
    {"id": "12345682", "desc": "Ineligible (Max Loans)", "amount": 1000, "term": 12, "expect": False},
    {"id": "12345683", "desc": "Eligible (High Earner)", "amount": 20000, "term": 24, "expect": True},
]

def test_loan(scenario):
    payload = {
        "national_id": scenario["id"],
        "loan_amount": scenario["amount"],
        "term_months": scenario["term"]
    }
    print(f"\nTesting: {scenario['desc']} (ID: {scenario['id']})")
    try:
        response = requests.post(BASE_URL, json=payload, timeout=5)
        data = response.json()
        
        eligible = data.get("eligible")
        print(f"Result: Eligible={eligible}, Reason='{data.get('reason', 'N/A')}'")
        
        if eligible == scenario["expect"]:
            print("✅ PASS")
        else:
            print(f"❌ FAIL (Expected {scenario['expect']})")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    for s in scenarios:
        test_loan(s)
