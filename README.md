# Professional Situation 2025-2026 - Security Audit Tool

## A. Description

This project is a comprehensive security audit tool built with FastAPI that provides network vulnerability scanning, audit reporting, and security analytics. It includes JWT-based authentication, Nmap integration for port scanning, automated PDF report generation, and a web-based interface for managing security audits.

## B. Key Features

- **Authentication System**: JWT token-based authentication with secure login
- **Network Scanning**: Port scanning using Nmap with service/version detection
- **Risk Assessment**: Automated vulnerability analysis and risk scoring
- **Report Generation**: Professional PDF reports with security findings
- **Data Management**: SQLite database for storing scan results and history
- **RESTful API**: Complete API for all operations with CORS support
- **Web Dashboard**: HTML-based frontend for users to interact with the tool
- **Background Jobs**: Asynchronous scan job processing
- **Statistics & Analytics**: Scan history tracking and statistical analysis
- **System Logging**: Comprehensive logging system for audit trails

## C. Project Structure

```
MSP_2025-2026/
├── backend/                    # FastAPI backend application
│   ├── main.py                # Application entry point and router configuration
│   ├── auth/
│   │   └── auth_handler.py    # JWT token creation and validation
│   ├── database/
│   │   └── db.py              # Database initialization and connection
│   ├── models/                # Data models (Pydantic schemas)
│   ├── routes/                # API endpoint handlers
│   │   ├── auth.py            # POST /login - User authentication
│   │   ├── health.py          # Database health check endpoints
│   │   ├── scan.py            # GET /scan - Initiate host scanning
│   │   ├── nmap_scan.py       # Nmap-specific scanning endpoints
│   │   ├── report.py          # Report retrieval and management
│   │   ├── history.py         # Scan history endpoints
│   │   ├── stats.py           # Statistics and analytics endpoints
│   │   └── logs.py            # System logs endpoints
│   └── services/              # Business logic and utilities
│       ├── scanner.py         # Core scanning orchestration
│       ├── nmap_scanner.py    # Nmap integration and execution
│       ├── jobs.py            # Background job processing
│       └── report_generator.py # PDF report creation using ReportLab
├── frontend/                  # Web-based user interface
│   └── pages/
│       ├── index.html         # Dashboard landing page
│       ├── dashboard.html     # Main dashboard interface
│       └── history.html       # Scan history view
├── logs_analyzer/             # Log analysis utilities
└── requirements.txt           # Python dependencies
```

## D. Technology Stack

- **Backend Framework**: FastAPI with Uvicorn ASGI server
- **Authentication**: Python-jose with cryptography
- **Network Scanning**: python-nmap (Nmap integration)
- **Report Generation**: ReportLab for PDF creation
- **Database**: SQLite
- **Frontend**: HTML/JavaScript
- **Middleware**: CORS support for cross-origin requests

## E. Installation & Setup

### E1. Prerequisites

- Python 3.8 or higher
- pip package manager
- Nmap installed on the system (available in PATH)
- Git for version control

### E2. Install Dependencies

From the project root directory:

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
- fastapi
- uvicorn
- python-jose
- python-nmap
- reportlab
- requests

### E3. Verify Nmap Installation

Ensure Nmap is installed and accessible:

```bash
nmap --version
```

If Nmap is not available, the application will display a warning on startup.

## F. Running the Application

### F1. Start the Backend

Navigate to the backend directory and run:

```bash
cd backend
python -m uvicorn main:app --reload
```

- Server runs on: `http://127.0.0.1:8000`
- Auto-reload is enabled for development
- Startup checks if Nmap is available

### F2. Access the Frontend

The frontend files are located in `frontend/pages/`:

```bash
cd frontend
python -m http.server 5500
```

- Frontend accessible at: `http://localhost:5500`

### F3. API Documentation

Once the backend is running, access interactive documentation:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## G. API Endpoints Reference

### G1. Authentication
- `POST /login` - User login (default: username: `admin`, password: `admin123`)
  - Returns JWT access token for authenticated requests

### G2. Scanning Operations
- `GET /scan?host={hostname}` - Perform security scan on specified host
- Nmap scanning endpoints for detailed service/version detection

### G3. Reports
- `GET /report` - Download generated PDF audit report

### G4. History & Analytics
- `GET /history` - Retrieve scan history (requires JWT token)
- `GET /stats` - Get audit statistics and analytics

### G5. Health Checks
- `GET /` - Application health check
- `GET /health` - Database and system health status

### G6. Logs
- `GET /logs` - Access system and audit logs

## H. Database

The application uses SQLite database (`audit.db`) for persistent data storage. The database is automatically initialized on first run.

### H1. Main Tables

The `scans` table stores:
- **id**: Primary key (unique identifier)
- **host**: Scanned hostname/IP address
- **ports**: Open ports (JSON format)
- **risque**: Risk assessment level
- **score**: Security score (0-100)
- **date_scan**: Timestamp of scan execution

### H2. Data Flow

1. User initiates scan via API
2. Scanner queries target host using Nmap
3. Results stored in SQLite database
4. Report generated from stored data
5. Statistics aggregated from historical data

## I. Security Considerations

### I1. Authentication
- Default credentials: username `admin`, password `admin123`
- **IMPORTANT**: Change these in production environments
- JWT tokens expire after 1 hour

### I2. Environment Hardening
- Change the `SECRET_KEY` in `backend/auth/auth_handler.py` for production
- Use HTTPS in production (configure via reverse proxy)
- Implement rate limiting on API endpoints
- Use environment variables for sensitive configuration

### I3. Nmap Execution
- Nmap requires appropriate system permissions
- Network scanning should comply with legal and policy requirements
- Only scan networks/hosts you own or have explicit permission to scan

## J. Development Guide

### J1. Project Architecture

The application follows a layered architecture:
- **Routes Layer** (`routes/`): HTTP endpoint definitions
- **Services Layer** (`services/`): Business logic and operations
- **Auth Layer** (`auth/`): Authentication and token management
- **Database Layer** (`database/`): Data persistence
- **Models Layer** (`models/`): Data structures and schemas

### J2. Adding New Routes

1. Create a new router file in `backend/routes/`
2. Define endpoints using FastAPI decorators
3. Import the router in `backend/main.py`
4. Include it with `app.include_router()`

Example:
```python
from fastapi import APIRouter
router = APIRouter()

@router.get("/new-endpoint")
def new_endpoint():
    return {"message": "New endpoint"}
```

### J3. Adding New Services

1. Create logic in `backend/services/`
2. Import and use in route handlers
3. Keep services independent and reusable

### J4. Testing

- Use `test_scanner.py` for scanner functionality testing
- Test all endpoints via Swagger UI at `/docs`
- Verify database connectivity and operations

## K. Troubleshooting

### K1. Backend Won't Start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (requires 3.8+)
- Verify port 8000 is not in use

### K2. Nmap Not Found Error
- Install Nmap: 
  - **Windows**: Download from https://nmap.org/download
  - **Linux**: `sudo apt-get install nmap`
  - **macOS**: `brew install nmap`
- Ensure Nmap is in system PATH
- Verify installation: `nmap --version`

### K3. Database Errors
- Delete `audit.db` to reset database
- Ensure write permissions in backend directory
- Check database initialization in `backend/database/db.py`

### K4. CORS Issues
- CORS is enabled for all origins in development (see `main.py`)
- Adjust `allow_origins` for production

### K5. JWT Token Errors
- Ensure `Authorization: Bearer <token>` header is included
- Check token expiration
- Verify token was generated via `/login` endpoint

## L. Frontend Components

Located in `frontend/pages/`:

- **index.html**: Landing page and authentication interface
- **dashboard.html**: Main dashboard for scan operations and results
- **history.html**: Historical scan data and statistics visualization

The frontend communicates with the FastAPI backend via REST API calls.

## M. Logs & Analytics

### M1. System Logs
- Accessible via `GET /logs` endpoint
- Tracks API operations, scans, and errors

### M2. Logs Analyzer
- The `logs_analyzer/` module provides log analysis utilities
- Useful for audit trails and debugging

## N. Future Enhancements

- [ ] Advanced log visualization dashboard
- [ ] Scheduled scan automation
- [ ] Multi-user support with role-based access control
- [ ] Enhanced reporting templates
- [ ] Real-time scan progress updates via WebSockets
- [ ] Vulnerability database integration
- [ ] Export reports in multiple formats (HTML, CSV, XML)

## O. Contributing & Support

### O1. Development Workflow
1. Create a feature branch from `main`
2. Implement changes with proper testing
3. Submit pull requests with clear descriptions
4. Ensure code follows project conventions

### O2. Reporting Issues
- Describe the issue clearly
- Include steps to reproduce
- Provide relevant log outputs
- Specify your environment (OS, Python version)

## P. License & Legal

This project is developed for educational purposes in a Professional Situation (2025-2026) context. 

**Legal Notice**: Network scanning can be illegal or unethical if performed without explicit authorization. Always:
- Obtain proper authorization before scanning any network or host
- Comply with applicable laws and regulations in your jurisdiction
- Use this tool responsibly for legitimate security testing only
- Review your organization's security policies

---

**Last Updated**: 2026-06-13