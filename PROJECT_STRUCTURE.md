# Advanced Traffic Management System - Project Structure

## Overview
The ATMS is a comprehensive traffic management platform leveraging AI and IoT technologies for real-time traffic monitoring, violation reporting, and intelligent fine adjustment.

## Directory Structure

```
advanced-traffic-management-system/
├── backend/                    # Django REST API backend
│   ├── atms/                  # Main Django project
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py            # URL routing
│   │   ├── wsgi.py            # WSGI configuration
│   │   └── __init__.py
│   ├── traffic_app/           # Traffic management app
│   │   ├── models.py          # Django models
│   │   ├── views.py           # ViewSets for API
│   │   ├── serializers.py     # DRF serializers
│   │   ├── urls.py            # App URLs
│   │   └── __init__.py
│   ├── manage.py              # Django management script
│   └── requirements.txt        # Python dependencies
│
├── frontend/                   # React.js frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   ├── store/             # Redux state management
│   │   ├── styles/            # CSS files
│   │   ├── App.js             # Main App component
│   │   └── index.js           # Entry point
│   ├── package.json           # Node dependencies
│   └── Dockerfile
│
├── docker-compose.yml         # Docker development setup
├── .gitignore                 # Git ignore rules
├── .env.example               # Environment variables template
├── README.md                  # Project documentation
└── PROJECT_STRUCTURE.md       # This file
```

## Key Features

### 1. Peer-to-Peer Reporting
- Citizens can report traffic violations directly
- Real-time notification system
- Community engagement dashboard

### 2. Intelligent Fine Adjustment
- Machine learning algorithms calculate fines based on:
  - Violation severity
  - Offender history
  - Financial status assessment
- Fair and transparent penalty system

### 3. Gamification & Rewards
- Points system for safe driving
- Badges and achievements
- Leaderboards and challenges
- Incentivizes community participation

## Technology Stack

### Backend
- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Task Queue**: Celery 5.3.4
- **ML Libraries**: scikit-learn, NumPy, SciPy

### Frontend
- **Framework**: React.js
- **State Management**: Redux
- **HTTP Client**: Axios
- **UI Library**: Material-UI or Bootstrap
- **Real-time**: WebSockets for live updates

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Version Control**: Git

## API Endpoints

### Core Resources
- `GET/POST /api/violations/` - Traffic violations
- `GET/POST /api/users/` - User management
- `GET/POST /api/reports/` - User reports
- `GET/POST /api/fines/` - Fine calculations

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- Node.js 16+

### Quick Start
```bash
# Clone repository
git clone https://github.com/Raghavendracharykurella/advanced-traffic-management-system
cd advanced-traffic-management-system

# Start with Docker Compose
docker-compose up

# Access applications
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Django Admin: http://localhost:8000/admin
```

## Contributing
Contributions are welcome! Please follow PEP 8 for Python and ESLint for JavaScript.

## License
MIT License
