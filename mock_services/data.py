MOCK_DATA = {
    "12345678": {
        "salary": {"monthly_salary": 5000, "currency": "USD"},
        "credit": {"credit_score": 750, "active_loans": 1, "active_defaults": False}
    },
    "12345679": {
        "salary": {"monthly_salary": 800, "currency": "USD"}, # Too low for meaningful loans
        "credit": {"credit_score": 700, "active_loans": 0, "active_defaults": False}
    },
    "12345680": {
        "salary": {"monthly_salary": 3000, "currency": "USD"},
        "credit": {"credit_score": 550, "active_loans": 0, "active_defaults": False} # Low score
    },
    "12345681": {
        "salary": {"monthly_salary": 3000, "currency": "USD"},
        "credit": {"credit_score": 650, "active_loans": 0, "active_defaults": True} # Default
    },
    "12345682": {
        "salary": {"monthly_salary": 3000, "currency": "USD"},
        "credit": {"credit_score": 650, "active_loans": 4, "active_defaults": False} # Too many loans
    },
    "12345683": {
        "salary": {"monthly_salary": 15000, "currency": "USD"}, # High earner
        "credit": {"credit_score": 850, "active_loans": 0, "active_defaults": False}
    },
    "12345684": {
        "salary": {"monthly_salary": 4000, "currency": "USD"},
        "credit": {"credit_score": 600, "active_loans": 1, "active_defaults": False} # Borderline score
    },
    "12345685": {
        "salary": {"monthly_salary": 4000, "currency": "USD"},
        "credit": {"credit_score": 700, "active_loans": 3, "active_defaults": False} # Max loans
    },
    "12345686": {
        "salary": {"monthly_salary": 2000, "currency": "USD"},
        "credit": {"credit_score": 720, "active_loans": 0, "active_defaults": False}
    },
    "12345687": {
        "salary": {"monthly_salary": 5555, "currency": "USD"},
        "credit": {"credit_score": 666, "active_loans": 2, "active_defaults": False}
    }
}
