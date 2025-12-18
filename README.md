# Youths4Change Backend API

Flask + PostgreSQL (Neon) REST API for the Youths4Change Initiative - A youth empowerment organization operating across 8 African countries.

## 🌍 Overview

This backend powers a comprehensive NGO management platform with features for project management, volunteer applications, donations, team management, content management, and analytics.

## 🚀 Tech Stack

- **Framework**: Flask 3.1.2
- **Database**: PostgreSQL (Neon Cloud)
- **Authentication**: Session-based with bcrypt
- **Image Storage**: Cloudinary integration
- **CORS**: Configured for cross-origin requests
- **Python**: 3.9+

## 📋 Prerequisites

- Python 3.9 or higher
- Neon PostgreSQL database account
- pip package manager

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/InaresKenne/youths4change-backend.git
cd youths4change-backend
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```env
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@host.neon.tech/youths4change?sslmode=require

# Security
SECRET_KEY=your-secure-random-secret-key-here

# Environment
FLASK_ENV=development
```

### 5. Run the server
```bash
python app.py
```

Server runs on `http://localhost:5001`

## 📚 API Documentation

### 🔐 Authentication
- `POST /api/auth/login` - Admin login (username, password)
- `POST /api/auth/logout` - Logout current session
- `GET /api/auth/me` - Get current admin info

### 📂 Projects
- `GET /api/projects` - Get all projects (with filters)
- `GET /api/projects/<id>` - Get single project
- `POST /api/projects` - Create new project (admin)
- `PUT /api/projects/<id>` - Update project (admin)
- `DELETE /api/projects/<id>` - Delete project (admin)

### 🖼️ Project Images (Gallery)
- `GET /api/projects/<id>/images` - Get all images for a project
- `POST /api/projects/<id>/images` - Add image to project gallery
- `PUT /api/projects/<id>/images/<image_id>` - Update image caption/order
- `DELETE /api/projects/<id>/images/<image_id>` - Delete image
- `PUT /api/projects/<id>/images/reorder` - Batch reorder images

### 📝 Applications
- `GET /api/applications` - Get all applications (admin)
- `POST /api/applications` - Submit volunteer application
- `GET /api/applications/<id>` - Get single application (admin)
- `PUT /api/applications/<id>/review` - Approve/reject application (admin)

### 💰 Donations
- `GET /api/donations` - Get all donations (admin)
- `POST /api/donations` - Record donation
- `GET /api/donations/<id>` - Get single donation (admin)
- `GET /api/donations/stats` - Get donation statistics (admin)

### 📊 Analytics
- `GET /api/analytics/overview` - Overall statistics dashboard
- `GET /api/analytics/projects-by-country` - Projects grouped by country
- `GET /api/analytics/countries` - List of active countries

### 👥 Team Management
- `GET /api/team/founders` - Get all founders
- `POST /api/team/founders` - Create founder profile (admin)
- `PUT /api/team/founders/<id>` - Update founder (admin)
- `DELETE /api/team/founders/<id>` - Delete founder (admin)
- `GET /api/team/members` - Get all team members
- `POST /api/team/members` - Create team member (admin)
- `PUT /api/team/members/<id>` - Update member (admin)
- `DELETE /api/team/members/<id>` - Delete member (admin)

### ⚙️ Settings & Content
- `GET /api/settings` - Get site settings
- `PUT /api/settings` - Update site settings (admin)
- `GET /api/page-content/<page>` - Get page content
- `PUT /api/page-content/<page>` - Update page content (admin)
- `GET /api/core-values` - Get core values
- `POST /api/core-values` - Create core value (admin)
- `PUT /api/core-values/<id>` - Update core value (admin)
- `DELETE /api/core-values/<id>` - Delete core value (admin)
- `GET /api/team-roles` - Get team roles
- `POST /api/team-roles` - Create role (admin)
- `PUT /api/team-roles/<id>` - Update role (admin)
- `DELETE /api/team-roles/<id>` - Delete role (admin)

### 📞 Contact Management
- `GET /api/contact-info` - Get contact information
- `PUT /api/contact-info/<id>` - Update contact info (admin)
- `GET /api/social-media` - Get active social media links
- `GET /api/social-media/all` - Get all social media (admin)
- `POST /api/social-media` - Create social media link (admin)
- `PUT /api/social-media/<id>` - Update social link (admin)
- `DELETE /api/social-media/<id>` - Delete social link (admin)
- `GET /api/regional-offices` - Get active regional offices
- `GET /api/regional-offices/all` - Get all offices (admin)
- `GET /api/regional-offices/countries` - Get list of countries
- `POST /api/regional-offices` - Create office (admin)
- `PUT /api/regional-offices/<id>` - Update office (admin)
- `DELETE /api/regional-offices/<id>` - Delete office (admin)

## 🗄️ Database Schema

### Tables
1. **admins** - Admin user accounts
2. **projects** - Project information
3. **project_images** - Project gallery images
4. **applications** - Volunteer applications
5. **donations** - Donation records
6. **site_settings** - Global site configuration
7. **page_content** - Dynamic page content
8. **core_values** - Organization values
9. **team_roles** - Available team positions
10. **contact_info** - Contact information
11. **social_media** - Social media links
12. **regional_offices** - Office locations
13. **founders** - Founder profiles
14. **team_members** - Team member profiles

## 🔒 Security Features

- Bcrypt password hashing
- Session-based authentication
- CSRF protection
- Input validation with regex patterns
- SQL injection prevention with parameterized queries
- CORS configuration for trusted origins
- HttpOnly session cookies

## 🛠️ Development

### Default Admin Credentials
```
Username: admin
Password: admin123
```
⚠️ Change these in production!

### Running Tests
```bash
python test_db.py
```

### Code Structure
```
youths4change-backend/
├── app.py                 # Main Flask application
├── config/
│   ├── __init__.py
│   └── database.py        # Database connection
├── routes/
│   ├── analytics.py       # Analytics endpoints
│   ├── applications.py    # Application management
│   ├── auth.py           # Authentication
│   ├── contact.py        # Contact management
│   ├── donations.py      # Donation tracking
│   ├── project_images.py # Project gallery
│   ├── projects.py       # Project CRUD
│   ├── settings.py       # Site settings
│   └── team.py           # Team management
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables
```

## 🌐 Deployment

### Render.com Deployment

1. Add to `requirements.txt`:
```
gunicorn==21.2.0
```

2. Create `render.yaml`:
```yaml
services:
  - type: web
    name: youths4change-backend
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: youths4change-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
```

3. Push to GitHub and connect to Render

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Authors

Youths4Change Development Team

## 🔗 Links

- Frontend Repository: [youths4change-frontend](https://github.com/InaresKenne/youths4change-frontend)
- Live Site: [Coming Soon]
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