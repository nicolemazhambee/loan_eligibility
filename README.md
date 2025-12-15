# Loan Eligibility API

A Django REST Framework API that evaluates loan applications based on salary, credit score, and other criteria.

## Features

- **Loan Application Endpoint**: `POST /api/loans/eligibility/`
- **Mock Services**:
    - Salary Verification: `GET /api/mocks/salary/<national_id>/`
    - Credit Bureau: `GET /api/mocks/credit/<national_id>/`
- **Eligibility Rules**:
    - Salary >= 3x Monthly Repayment
    - Credit Score >= 600
    - No active defaults
    - Max 3 active loans

## Tech Choices

- **Django & DRF**: Standard, robust framework for Python APIs.
- **Internal Mocks**: Mock services are implemented as a separate Django app but deployed together for simplicity.
- **Random Deterministic Data**: Mocks use `random.seed(national_id)` to ensure consistent results for testing without a database.

## How to Run Locally

1. **Clone the repository** (or unzip).
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```
5. **Start the server**:
   ```bash
   python manage.py runserver
   ```

## API Usage

**Check Eligibility:**

POST `http://127.0.0.1:8000/api/loans/eligibility/`

```json
{
  "national_id": "12345",
  "loan_amount": 5000,
  "term_months": 12
}
```

## Improvements for Production

- **Authentication**: Add JWT or API Key authentication via `djangorestframework-simplejwt`.
- **Database**: Use PostgreSQL instead of SQLite.
- **Async**: Use `aiohttp` or `httpx` for non-blocking calls to external services.
- **Caching**: Cache credit/salary checks using Redis.
- **Monitoring**: Add Sentry for error tracking.
