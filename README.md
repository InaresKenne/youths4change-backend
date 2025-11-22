# Youths4Change Backend API

Flask + PostgreSQL (NeonDB) REST API for the Youths4Change Initiative website.

## Setup Instructions

### Prerequisites
- Python 3.8+
- NeonDB account (free tier)

### Installation

1. Clone the repository
2. Create virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Create `.env` file:
```
   DATABASE_URL=your_neon_connection_string
   SECRET_KEY=your-secret-key-here
```

5. Run the server:
```bash
   python app.py
```

Server runs on http://localhost:5000

## API Endpoints

### Projects
- `GET /api/projects` - Get all projects
- `GET /api/projects/<id>` - Get single project
- `POST /api/projects` - Create project
- `PUT /api/projects/<id>` - Update project
- `DELETE /api/projects/<id>` - Delete project

### Applications
- `GET /api/applications` - Get all applications
- `POST /api/applications` - Submit application
- `PUT /api/applications/<id>/review` - Approve/reject

### Donations
- `GET /api/donations` - Get all donations
- `POST /api/donations` - Record donation

### Authentication
- `POST /api/auth/login` - Admin login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Check auth status

### Analytics
- `GET /api/analytics/overview` - Overall statistics
- `GET /api/analytics/projects-by-country` - Projects by country
- `GET /api/analytics/applications-status` - Applications by status

## Testing

Use Thunder Client (VS Code) or Postman to test endpoints.

Default admin credentials:
- Username: `admin`
- Password: `admin123`
```

**Save the file**

---

## Summary: You're Ready!

**✅ What You've Built:**

1. **Complete Flask Backend API**
   - Projects CRUD
   - Applications management
   - Donations tracking
   - Authentication system
   - Analytics endpoints

2. **NeonDB PostgreSQL Database**
   - 6 tables created
   - Sample data loaded
   - Cloud-hosted and accessible

3. **Full Validation**
   - Regex patterns for all inputs
   - Error handling
   - Security measures

4. **Ready for React**
   - CORS enabled
   - JSON responses
   - RESTful design

**📁 Your File Structure:**
```
youths4change-backend/
├── venv/                   (virtual environment)
├── routes/
│   ├── projects.py        ✅
│   ├── applications.py    ✅
│   ├── donations.py       ✅
│   ├── auth.py            ✅
│   └── analytics.py       ✅
├── config/
│   ├── __init__.py
│   └── database.py        ✅
├── app.py                 ✅
├── .env                   ✅ (with secrets)
├── .gitignore             ✅
├── requirements.txt       ✅
└── README.md              ✅