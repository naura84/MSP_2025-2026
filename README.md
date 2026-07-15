# AI-Powered Network Security Audit Platform

This project is an AI-assisted network security audit platform designed to automate vulnerability discovery, risk prioritization and remediation recommendations. It combines FastAPI, Nmap and local LLM inference (Ollama) to produce actionable security reports.

## 1. Key Features

- JWT authentication with default credentials (`admin` / `admin123`)
- Host scanning through the `/scan` endpoint
- Advanced scanning with Nmap supporting `ip` and `url` inputs
- Background scan tracking through `/nmap_scan` and `/nmap_scan/{job_id}`
- Scan history stored in a SQLite database
- Global scan statistics
- PDF report generation
- AI-based security recommendations through an integrated advisor module
- Deletion of a specific scan entry
- Database and service health verification

## 2. Project Structure

```text
AI-Powered Network Security Audit Platform/
├── backend/
│   ├── auth/
│   │   └── auth_handler.py       # JWT token creation and validation
│   ├── core/
│   │   └── logger.py             # logging configuration
│   ├── database/
│   │   └── db.py                 # SQLite database initialization
│   ├── logs/
│   │   └── audit.log             # audit log file
│   ├── routes/
│   │   ├── auth.py               # POST /login
│   │   ├── health.py             # GET /health
│   │   ├── scan.py               # GET /scan
│   │   ├── nmap_scan.py          # POST /nmap_scan and job tracking
│   │   ├── history.py            # GET /history
│   │   ├── stats.py              # GET /stats
│   │   ├── report.py             # GET /report and /report/{scan_id}
│   │   ├── delete_scans.py       # DELETE /delete_scans/{scan_id}
│   │   └── ai_advi.py            # POST /recommendations for AI advice
│   ├── services/
│   │   ├── scanner.py            # standard scan logic
│   │   ├── nmap_scanner.py       # Nmap integration and risk evaluation
│   │   ├── report_generator.py   # PDF generation
│   │   ├── ai_advisor.py         # AI recommendations based on scan results
│   │   └── test_scanner.py       # manual test script
│   └── main.py                   # FastAPI entry point
├── frontend/
│   └── pages/
│       ├── index.html
│       ├── dashboard.html
│       └── history.html
└── requirements.txt
```

## 3. Technical Stack

- Backend: FastAPI + Uvicorn
- Authentication: JWT (python-jose)
- Network scanning: Nmap via `python-nmap`
- Report generation: ReportLab
- AI recommendations: Ollama via HTTP requests
- Database: SQLite
- Frontend: static HTML pages

## 4. Prerequisites

- Python 3.10+
- `pip`
- Nmap installed and available in the `PATH`
- Ollama installed and running locally for AI recommendations
- Git

## 5. Installation

```bash
pip install -r requirements.txt
```

## 6. Running the Application

### 6.1 Backend

```bash
cd backend
python -m uvicorn main:app --reload
```

The server will be available at:
- http://127.0.0.1:8000

### 6.2 Frontend

```bash
cd frontend
python -m http.server 5500
```

The frontend will be available at:
- http://localhost:5500

### 6.3 API Documentation

Once the backend is running:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 7. Main Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/login` | User authentication |
| GET | `/scan?host={host}` | Launches a scan against a target |
| POST | `/nmap_scan` | Starts a background Nmap scan |
| GET | `/nmap_scan/{job_id}` | Checks the status of a job |
| POST | `/recommendations` | Generates AI-based security recommendations from scan results |
| GET | `/history` | Retrieves scan history |
| GET | `/stats` | Returns overall statistics |
| GET | `/report` | Downloads the global PDF report |
| GET | `/report/{scan_id}` | Downloads the report for a specific scan |
| DELETE | `/delete_scans/{scan_id}` | Deletes a scan |
| GET | `/health` | Checks the service and database status |

## 8. Database

The project uses SQLite with the `audit.db` database, which is created automatically at startup if it does not already exist.

The main fields stored in the `scans` table are:
- `id`
- `host`
- `type`
- `ports`
- `risque`
- `score`
- `date_scan`
- `service`
- `detected_version`
- `cve`
- `severity`
- `description`

## 9. Important Notes

- Default credentials should be changed in production.
- The JWT secret is currently defined in [backend/auth/auth_handler.py](backend/auth/auth_handler.py).
- AI recommendations require a running local Ollama service and a compatible model.
- Network scanning must comply with local laws and authorization requirements.
- If Nmap is not available, the application will display a warning at startup.

## 10. Development

To test or develop the project:
1. Verify that the dependencies are installed.
2. Start the backend in development mode.
3. Test the routes through `/docs`.
4. Check the logs in [backend/logs](backend/logs).

## 11. Engineering Challenges

- Designing an asynchronous scan workflow

- Computing dynamic risk scores

- Integrating AI recommendations without slowing scans

- Detecting vulnerable versions through CVE mapping

- Structuring a layered FastAPI architecture

## 12. License and Legal Notice

This project is developed for educational purposes in a professional context for 2025-2026.

**Legal Notice**: Network scanning can be illegal or unethical if performed without explicit authorization. Always:
- Obtain proper authorization before scanning any network or host.
- Comply with applicable laws and regulations in your jurisdiction.
- Use this tool responsibly for legitimate security testing only.
- Review your organization’s security policies.

---

**Last Updated**: 2026-07-15
