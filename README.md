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

## Test Subjects (Mock Data)

You can use the following National IDs to test various eligibility scenarios:

| National ID | Scenario | Salary | Credit Score | Active Loans | Defaults |
|---|---|---|---|---|---|
| `12345678` | **Eligible** (Standard) | $5,000 | 750 | 1 | No |
| `12345679` | **Ineligible** (Low Salary) | $800 | 700 | 0 | No |
| `12345680` | **Ineligible** (Low Credit) | $3,000 | 550 | 0 | No |
| `12345681` | **Ineligible** (Active Default) | $3,000 | 650 | 0 | Yes |
| `12345682` | **Ineligible** (Too Many Loans) | $3,000 | 650 | 4 | No |
| `12345683` | **Eligible** (High Earner) | $15,000 | 850 | 0 | No |
| `12345684` | **Eligible** (Borderline Credit) | $4,000 | 600 | 1 | No |
| `12345685` | **Eligible** (Max Loans) | $4,000 | 700 | 3 | No |
| `12345686` | **Ineligible** (Mismatch) | $2,000 | 720 | 0 | No |
| `12345687` | **Ineligible** (Random) | $5,555 | 666 | 2 | No |

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
  "national_id": "12345678",
  "loan_amount": 5000,
  "term_months": 12
}
```

## Security & Authentication Note

**Why is Authentication Omitted?**

For the purposes of this technical assessment, authentication (JWT/OAuth) has been intentionally omitted to prioritize:

1.  **Reviewer Accessibility**: Removing auth barriers allows for immediate, frictionless testing of the core business logic using tools like Postman or cURL without needing to generate tokens first.
2.  **Scope Focus**: The assignment emphasizes the implementation of loan eligibility logic (Salary vs. Repayment, Credit Scores, etc.) and mock service integration. Adding a full auth layer would add boilerplate code not central to demonstrating the requested algorithmic skills.
3.  **Microservice Context**: In a real-world architecture, this service would likely sit behind an **API Gateway** (e.g., Kong, AWS API Gateway) which handles termination of SSL and Authentication. This service would then rely on passed-through headers or internal network security, treating the request as trusted (or validated via an internal token).

*Note: For a production-ready implementation, `djangorestframework-simplejwt` would be the standard choice for securing endpoints.*

## Improvements for Production

- **Authentication**: Add JWT or API Key authentication via `djangorestframework-simplejwt`.
- **Database**: Use PostgreSQL instead of SQLite.
- **Async**: Use `aiohttp` or `httpx` for non-blocking calls to external services.
- **Caching**: Cache credit/salary checks using Redis.
- **Monitoring**: Add Sentry for error tracking.
