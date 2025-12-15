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

### 1. Framework: Django & Django REST Framework (DRF)
- **Why?**: Django provides a robust, "batteries-included" foundation that excels at rapid development. DRF offers powerful tools for building Web APIs, including serializers for complex data validation and a browsable API interface for easy testing.
- **Benefit**: Allows focus on business logic (credit rules) rather than boilerplate (routing, ORM setup).

### 2. Architecture: Monolithic with Logical Separation
- **Implementation**: The project is structured as a single Django project with two distinct apps: `loans` (core business logic) and `mock_services` (external dependencies).
- **Why?**: This simulates a microservices capability while keeping deployment simple (single container/process). It allows `mock_services` to be easily decoupled and replaced with real integration clients in the future.

### 3. Data Storage: SQLite (Development)
- **Why?**: Chosen for zero-configuration setup to ensure the project runs immediately after cloning.
- **Trade-off**: Not suitable for high-concurrency production but perfect for this assessment's scope.

### 4. Deterministic Mocks
- **Implementation**: Mock services use `random.seed(national_id)`.
- **Why?**: This allows repeatable testing (e.g., ID `12345678` *always* returns the same salary) without the overhead of managing a persistent "mock database" state.

## How to Run Locally

### Prerequisites
- Python 3.8+ installed (`python --version`)
- pip installed (`pip --version`)
- Git installed (optional, for cloning)

### Step-by-Step Guide

1.  **Clone the repository** (or extract the zip):
    ```bash
    git clone <your-repo-url>
    cd nicole_mazhambe
    ```

2.  **Create a virtual environment**:
    *It is highly recommended to use a virtual environment to avoid conflicting package versions.*
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run migrations**:
    *Initialize the database schema.*
    ```bash
    python manage.py migrate
    ```

5.  **Start the development server**:
    ```bash
    python manage.py runserver
    ```
    You should see output indicating the server is running at `http://127.0.0.1:8000/`.

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

If additional time were available, the following improvements would be prioritized to move from "Assessment Prototype" to "Production Ready":

### 1. Robust Authentication & Authorization
- **Current**: No auth (for ease of review).
- **Proposed**: Implement **JWT Authentication** (JSON Web Tokens) using `djangorestframework-simplejwt`. This would allow stateless authentication suitable for scaling.
- **Role-Based Access**: Restrict `mock_services` endpoints to admin users or internal service accounts only, while allowing public access (or applicant access) to `loans`.

### 2. Database Upgrade
- **Current**: SQLite.
- **Proposed**: Migrate to **PostgreSQL**.
- **Why?**: Strict data integrity, better concurrent performance, and support for advanced JSON queries if needed for storing flexible loan metadata.

### 3. Asynchronous Task Processing
- **Current**: Synchronous blocking calls to salary/credit services.
- **Proposed**: Use **Celery** with Redis/RabbitMQ.
- **Why?**: External API calls can be slow. Moving them to a background task avoids blocking the main HTTP web thread, allowing the API to handle thousands of requests per second. The client would receive a "Application Received" (202 Accepted) response and check status via a polling endpoint or Webhook.

### 4. Containerization (Docker)
- **Proposed**: Add a `Dockerfile` and `docker-compose.yml`.
- **Benefit**: Guarantees the application runs exactly the same in development, staging, and production, eliminating "it works on my machine" issues.

### 5. Enhanced Monitoring & Logging
- **Proposed**: Integrate **Sentry** for crash reporting and **Prometheus/Grafana** for metrics (latency, error rates).
- **Why?**: Crucial for observing the health of the loan decision engine in real-time.
