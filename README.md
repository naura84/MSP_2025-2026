# Professional Situation 2025-2026 - Security Audit Tool

## Description

This project is a security audit tool that provides a FastAPI-based backend for scanning network hosts, generating security reports, and managing audit data. It includes authentication, scanning services, report generation, and statistical analysis.

## Features

- **Authentication**: JWT-based login system
- **Network Scanning**: Port scanning for common services (FTP, SSH, HTTP, HTTPS)
- **Risk Assessment**: Automatic risk scoring based on open ports
- **Report Generation**: PDF reports using ReportLab
- **Database**: SQLite-based data storage
- **API Endpoints**: RESTful API for all operations

## Project Structure

```
MSP_2025-2026/
├── backend/                 # FastAPI backend
│   ├── main.py             # Application entry point
│   ├── auth/               # Authentication handlers
│   ├── database/           # Database setup and models
│   ├── models/             # Data models
│   ├── routes/             # API route handlers
│   │   ├── auth.py         # Authentication endpoints
│   │   ├── scan.py         # Scanning endpoints
│   │   ├── report.py       # Report endpoints
│   │   ├── history.py      # Scan history
│   │   ├── stats.py        # Statistics
│   │   └── logs.py         # Logging
│   └── services/           # Business logic
│       ├── scanner.py      # Port scanning logic
│       └── report_generator.py # PDF generation
├── frontend/               # Frontend application (placeholder)
└── logs_analyzer/          # Logs analyzer (placeholder)
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Backend Dependencies

Install the required Python packages:

```bash
# FastAPI framework
pip install fastapi

# ASGI server for running FastAPI
pip install uvicorn

# JWT token handling
pip install python-jose[cryptography]

# PDF report generation
pip install reportlab
```

### Alternative: Using requirements.txt

Create a `requirements.txt` file in the backend directory with the following content:

```
fastapi
uvicorn
python-jose[cryptography]
reportlab
```

Then install all dependencies:

```bash
pip install -r requirements.txt
```

## Running the Project

### Backend

1. Navigate to the backend directory:

```bash
cd backend
```

2. Start the FastAPI server with auto-reload:

```bash
python -m uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### API Documentation

Once the server is running, visit `http://127.0.0.1:8000/docs` for interactive API documentation (Swagger UI).

## API Endpoints

### Authentication
- `POST /login` - User login (username: admin, password: admin123)

### Scanning
- `GET /scan?host={hostname}` - Perform security scan on a host

### Reports
- `GET /report` - Generate PDF audit report

### History
- `GET /history` - Get scan history

### Statistics
- `GET /stats` - Get audit statistics

### Health Check
- `GET /` - Application health check

## Database

The application uses SQLite database (`audit.db`) to store scan results. The database is automatically created on first run.

## Security Notes

- Default credentials: username `admin`, password `admin123`
- JWT tokens expire after 1 hour
- Change the `SECRET_KEY` in `auth/auth_handler.py` for production use

## Development

### Adding New Routes

1. Create a new router in `routes/`
2. Import and include it in `main.py`
3. Add business logic in `services/` if needed

### Database Schema

The main table `scans` stores:
- id: Primary key
- host: Scanned hostname/IP
- ports: Open ports (JSON string)
- risque: Risk assessment
- score: Security score (0-100)
- date_scan: Scan timestamp

## Frontend and Logs Analyzer

The `frontend/` and `logs_analyzer/` directories are currently placeholders for future development of:
- Web interface for the audit tool
- Log analysis and visualization components

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Use responsibly and in compliance with applicable laws and regulations.