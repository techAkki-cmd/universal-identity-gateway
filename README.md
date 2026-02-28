# Universal Identity & Data Gateway

This project is a centralized, stateless API Gateway built with Python and FastAPI.

The core idea behind this gateway is simple:  
separate **Identity Management** from **Data Ingestion**, while still allowing downstream systems to receive flexible, schema-less JSON data securely.

---

## Part 1 — Architecture & Zero-Trust Model

The gateway follows a strict **Zero-Trust identity model**.

Rather than trusting requests based on network location or internal IDs, every request must carry a valid JWT token issued by the authentication endpoint.

### Privacy by Design

This system was intentionally designed to protect user identity.

1. **Anonymous Tokens**  
   The JWT contains **no personal information**.  
   It only includes:
   - `sub` → an anonymous UUID
   - `scopes` → namespaces the entity is allowed to access

2. **UUID Stamping**  
   When data is ingested:
   - The token is verified.
   - The anonymous UUID is extracted.
   - That UUID is attached to the incoming data record.

3. **Fully Decoupled Identity**  
   Downstream systems (databases, analytics services, etc.) can group data by this UUID —  
   but they never receive names, emails, or any real-world identity information.

In short, the system knows **which entity** sent the data —  
but never knows **who the person actually is**.

---

## Part 2 — Setup & Deployment

The application is fully containerized for easy local deployment.

### Prerequisites

- Docker  
- Docker Compose  

### Running the Gateway

Clone the repository and move into the project directory.

Then run:

```bash
docker-compose up --build
```

Once the container starts, the API will be available at:

```
http://localhost:8000
```

---

## Part 3 — Testing & Verification

You can test the ingestion endpoint in two ways:

- Using the interactive Swagger UI (recommended for quick visual testing)
- Using terminal-based `curl` commands

Both approaches demonstrate how the same endpoint can handle both flat and deeply nested JSON payloads without predefined schemas.

---

## Method A — Testing via Swagger UI

FastAPI automatically generates interactive API documentation.

1. Open your browser:
   ```
   http://localhost:8000/docs
   ```

2. Generate a Token:
   - Scroll to `POST /auth/token`
   - Click **Try it out**
   - Use:

```json
{
  "username": "admin",
  "password": "password123"
}
```

3. Copy the `access_token` from the response.

4. Click the **Authorize** button at the top of the page.
   - Paste the token
   - Click **Authorize**

5. Scroll to `POST /data/ingest`
   - Click **Try it out**
   - Test with either of the example payloads below.

---

## Method B — Testing via Terminal (curl)

### Step 1 — Generate Token

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password123"
  }'
```

Copy the `access_token` from the response.

---

### Step 2 — Scenario A: Simple Data (Database Scope)

Replace `YOUR_TOKEN_HERE` with the copied token.

```bash
curl -X POST http://localhost:8000/data/ingest \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "source_namespace": "Database",
    "metric_category": "biometric_log",
    "timestamp": "2026-02-28T12:00:00Z",
    "payload": {
      "heart_rate_bpm": 75
    }
  }'
```

---

### Step 3 — Scenario B: Complex Nested Object (Service Scope)

The same endpoint dynamically accepts deeply nested arrays and objects.

```bash
curl -X POST http://localhost:8000/data/ingest \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "source_namespace": "service",
    "metric_category": "engine_diagnostics",
    "timestamp": "2026-02-28T12:05:00Z",
    "payload": {
      "device_status": "online",
      "metadata": {
        "firmware": "v2.1",
        "calibration_required": false
      },
      "sensor_readings": [
        {"id": "s1", "temps": [45.2, 46.1, 44.8]},
        {"id": "s2", "temps": [39.1, 40.0, 41.2]}
      ]
    }
  }'
```

---

## What This Project Demonstrates

- Stateless API architecture  
- JWT-based Zero-Trust authentication  
- Strict separation of identity and data  
- Schema-agnostic ingestion  
- Support for deeply nested JSON  
- Clean Docker-based deployment  

---

