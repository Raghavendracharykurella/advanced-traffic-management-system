# Advanced Traffic Management System

AI-powered traffic management system with peer-to-peer reporting, intelligent fine adjustment, and gamification features. Built with Django backend and ReactJS frontend.

## Features

- 🚦 **Real-time Traffic Monitoring**: IoT sensor integration for live traffic data
- 📸 **Peer-to-Peer Reporting**: Community-driven violation reporting with photo evidence
- 🤖 **AI-Powered Analysis**: Intelligent fine adjustment based on context and history
- 🎮 **Gamification**: Points, badges, and leaderboards to encourage participation
- 📊 **Data Analytics**: Comprehensive dashboard with charts and statistics
- 🔒 **Secure Authentication**: JWT-based user authentication
- 📱 **Responsive Design**: Mobile-friendly interface

## Technology Stack

### Backend
- Python 3.x
- Django 4.x
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Celery (for async tasks)

### Frontend
- React 18.x
- React Router
- Axios
- Recharts (for data visualization)
- CSS3

### DevOps
- Docker
- Docker Compose

## Project Structure

```
advanced-traffic-management-system/
├── backend/
│   ├── traffic_management/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── traffic_app/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.js
│   │   │   ├── ReportViolation.js
│   │   │   ├── Leaderboard.js
│   │   │   ├── Login.js
│   │   │   └── Profile.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.js
│   │   └── index.css
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Docker (optional)

### Method 1: Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/Raghavendracharykurella/advanced-traffic-management-system.git
cd advanced-traffic-management-system
```

2. Start services with Docker Compose:
```bash
docker-compose up -d
```

3. Run migrations:
```bash
docker-compose exec backend python manage.py migrate
```

4. Create superuser:
```bash
docker-compose exec backend python manage.py createsuperuser
```

5. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

### Method 2: Manual Setup

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure database in `traffic_management/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'traffic_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Start development server:
```bash
python manage.py runserver
```

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh access token

### Violations
- `GET /api/violations/` - List all violations
- `POST /api/violations/` - Report new violation
- `GET /api/violations/{id}/` - Get violation details
- `POST /api/violations/{id}/verify/` - Verify violation

### User Profile
- `GET /api/profiles/me/` - Get current user profile
- `GET /api/profiles/leaderboard/` - Get leaderboard

### Traffic Patterns
- `GET /api/patterns/` - Get traffic pattern analysis
- `GET /api/patterns/predict/` - AI-based prediction

### IoT Sensors
- `GET /api/sensors/` - List all sensors
- `GET /api/sensors/{id}/data/` - Get sensor data

## Usage

### Reporting a Violation
1. Navigate to "Report Violation" page
2. Fill in violation details:
   - Violation type (speeding, red light, etc.)
   - Vehicle number
   - Location
   - Upload photo evidence (optional)
3. Submit the report
4. Earn points when your report is verified!

### Viewing Dashboard
- See real-time statistics
- View charts showing violation trends
- Monitor your user stats

### Checking Leaderboard
- View top contributors
- See your ranking
- Track points and badges

## Gamification System

### Points
- Submit verified report: +10 points
- Add photo evidence: +5 bonus points
- First report of the day: +3 points

### Badges
- **Bronze**: 0-50 points
- **Silver**: 51-100 points
- **Gold**: 101-200 points
- **Platinum**: 201+ points

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

**Developer**: Raghavendra Charya Kurella
**GitHub**: [@Raghavendracharykurella](https://github.com/Raghavendracharykurella)
**Project Link**: [Advanced Traffic Management System](https://github.com/Raghavendracharykurella/advanced-traffic-management-system)

## Acknowledgments

- Django REST Framework documentation
- React documentation
- Recharts for data visualization
- Community contributors
