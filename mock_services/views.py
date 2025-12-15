import random
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def salary_verification(request, national_id):
    """
    Returns a deterministic salary based on the national_id.
    """
    # Use national_id to seed random generator for consistent results
    try:
        seed_val = int(national_id) if national_id.isdigit() else hash(national_id)
    except:
        seed_val = 0
        
    random.seed(seed_val)
    
    # Generate a salary between 1000 and 10000
    salary = random.randint(1000, 10000)
    
    return Response({
        "national_id": national_id,
        "monthly_salary": salary,
        "currency": "USD"
    })

@api_view(['GET'])
def credit_check(request, national_id):
    """
    Returns a deterministic credit score and history based on national_id.
    """
    try:
        seed_val = int(national_id) if national_id.isdigit() else hash(national_id)
    except:
        seed_val = 0
        
    random.seed(seed_val)
    
    credit_score = random.randint(300, 850)
    active_loans = random.randint(0, 5)
    active_defaults = random.choice([True, False, False, False]) # 25% chance of default
    
    return Response({
        "national_id": national_id,
        "credit_score": credit_score,
        "active_loans": active_loans,
        "active_defaults": active_defaults
    })
