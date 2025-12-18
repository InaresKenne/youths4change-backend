# Youths4Change Backend API

Flask + PostgreSQL (Neon) REST API for the Youths4Change Initiative - A youth-led nonprofit operating across 8 African countries.

## 🎯 Problem Statement

**The Challenge:**  
Youths4Change Initiative has been facing a critical challenge: **limited visibility and credibility** due to the absence of an official website. As a youth-led nonprofit operating in eight countries (Ghana, Nigeria, Kenya, Uganda, Tanzania, Rwanda, Zambia, and South Africa), the organization struggled with:

- ❌ **No centralized platform** to showcase impactful projects like EmpowerHer, GreenFuture, Back to School Campaign, and Mentorship Programs
- ❌ **Lack of credibility** when approaching partners, donors, and stakeholders
- ❌ **Fragmented data management** across 8 countries with no unified database
- ❌ **Difficult coordination** between country chapters
- ❌ **Limited fundraising capabilities** without a secure donation system
- ❌ **Inefficient recruitment** for volunteers and executive team members

**The Solution:**  
This backend powers a comprehensive multi-country database and web platform that serves as a **central hub for communication, recruitment, partnership, and fundraising**. The platform solves these problems by:

✅ **Centralized Database System** - Unified data management across all 8 countries  
✅ **Project Showcase** - Display and track impact of all community projects  
✅ **Secure Donation System** - Manual payment verification for Mobile Money and Bank Transfers  
✅ **Volunteer Applications** - Streamlined application and approval process  
✅ **Team Management** - Organized profiles for founders, executives, and members  
✅ **Dynamic Content** - Customizable website content without code changes  
✅ **Analytics Dashboard** - Real-time insights on donations, projects, and engagement  
✅ **Multi-Country Coordination** - Regional offices and country-specific data tracking

## 🌍 Overview

This REST API powers the Youths4Change Initiative website with comprehensive features for:
- **Project Management** - CRUD operations for community projects with image galleries
- **Donation Processing** - Manual payment verification with Mobile Money & Bank Transfer support
- **Volunteer Applications** - Application submission and review workflow
- **Team Management** - Founder, executive, and member profile management
- **Content Management** - Dynamic page content, settings, and core values
- **Analytics & Reporting** - Donation statistics, project tracking, and country-level insights
- **Contact Management** - Regional offices, social media, and contact information

## 🚀 Tech Stack

- **Framework**: Flask 3.1.2
- **Database**: PostgreSQL 16 (Neon Cloud - Serverless)
- **Authentication**: Session-based with bcrypt password hashing
- **Image Storage**: Cloudinary integration for project galleries and team photos
- **Payment Methods**: Manual verification for Mobile Money & Bank Transfers
- **Deployment**: Render.com with auto-deploy from GitHub
- **CORS**: Configured for Vercel frontend (production) and localhost (development)
- **Python**: 3.9.6+

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

### 💰 Donations (Manual Payment System)
- `GET /api/donations` - Get all donations with filters (admin)
- `POST /api/donations` - Submit donation with payment details
- `GET /api/donations/<id>` - Get single donation (admin)
- `GET /api/donations/stats` - Get verified donation statistics (admin)
- `PUT /api/donations/<id>/verify` - Verify payment (admin)
- `PUT /api/donations/<id>/reject` - Reject payment with reason (admin)
- `GET /api/donations/payment-accounts` - Get Mobile Money & Bank account details

**Supported Payment Methods:**
- Mobile Money (MTN, Vodafone, AirtelTigo)
- Bank Transfer (Ecobank Ghana)

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

### Core Tables (16 Total)
1. **admins** - Admin user accounts with bcrypt authentication
2. **projects** - Project information with country tracking
3. **project_images** - Multi-image gallery per project with Cloudinary integration
4. **applications** - Volunteer application submissions with review workflow
5. **donations** - Donation records with manual payment verification
   - Fields: `payment_method`, `transaction_id`, `payment_proof_url`, `payment_status`, `verified_by`, `verified_at`, `verification_notes`
6. **site_settings** - Global site configuration (hero text, mission, vision, payment accounts)
7. **page_content** - Dynamic page content for About, Apply, Contact pages
8. **core_values** - Organization core values with icons
9. **team_roles** - Available team positions and responsibilities
10. **contact_info** - Contact methods (email, phone, address)
11. **social_media** - Social media platform links
12. **regional_offices** - 8 country office locations
13. **founder** - Founder profile with bio and social links
14. **team_members** - Team member profiles (executive, board, volunteers, advisors)
15. **members** - General membership records
16. **countries** - Country list with member counts and active projects

### Key Relationships
- `donations.project_id` → `projects.id` (Many-to-One)
- `donations.verified_by` → `admins.id` (Many-to-One)
- `project_images.project_id` → `projects.id` (Many-to-One, CASCADE delete)
- `project_images.uploaded_by` → `admins.id` (Many-to-One)

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
├── app.py                      # Main Flask application with CORS config
├── config/
│   ├── __init__.py
│   └── database.py             # PostgreSQL connection (Neon)
├── routes/
│   ├── analytics.py            # Analytics & dashboard statistics
│   ├── applications.py         # Volunteer application CRUD
│   ├── auth.py                 # Admin authentication & sessions
│   ├── contact.py              # Contact info, social media, regional offices
│   ├── donations.py            # Manual payment verification system
│   ├── projects.py             # Project CRUD operations
│   ├── settings.py             # Site settings & page content
│   └── team.py                 # Founder & team member management
├── models/                     # (Future: SQLAlchemy models)
├── utils/                      # (Future: Helper functions)
├── requirements.txt            # Python dependencies
├── test_db.py                  # Database connection test
├── youths4change_backup.sql    # Database schema with sample data
├── .env                        # Environment variables (not in Git)
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
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

## 🌟 Key Features Implemented

### 1. Manual Payment Verification System
- Support for Mobile Money (MTN, Vodafone, AirtelTigo) and Bank Transfer payments
- Transaction reference tracking
- Payment proof upload via Cloudinary
- Admin verification/rejection workflow with notes
- Only verified donations count toward statistics
- Currency support: USD with GHS conversion (1 USD = 15.5 GHS)

### 2. Multi-Country Data Management
- Centralized database for 8 African countries
- Country-specific project tracking
- Regional office management
- Country-based donation and application filtering

### 3. Project Gallery System
- Multiple images per project via Cloudinary
- Image reordering and caption management
- Batch upload support
- Automatic thumbnail generation

### 4. Dynamic Content Management
- Editable hero section, mission, and vision statements
- Customizable core values with icons
- Flexible page content for About, Apply, Contact pages
- Payment account settings (bank and mobile money)

### 5. Real-Time Analytics
- Donation statistics by country and project (verified only)
- Project distribution across countries
- Application status tracking
- Member count by country

## 📈 Impact & Results

By implementing this backend API, Youths4Change Initiative has achieved:

✅ **Enhanced Credibility** - Professional online presence for partnerships and funding applications  
✅ **Centralized Operations** - Single database managing data from 8 countries  
✅ **Improved Fundraising** - Secure donation system with payment verification  
✅ **Streamlined Recruitment** - Efficient volunteer application processing  
✅ **Better Coordination** - Real-time project tracking across all countries  
✅ **Data-Driven Decisions** - Analytics dashboard for impact measurement  
✅ **Scalability** - Cloud infrastructure (Neon + Render) supporting growth

**Projects Showcased:**
- EmpowerHer (Women's Empowerment)
- GreenFuture (Environmental Sustainability)
- Back to School Campaign (Education Access)
- Mentorship Program (Youth Development)
- Community Health Initiatives
- Skills Training Workshops

## 👨‍💻 Authors

**Youths4Change Development Team**
- Lead Developer: Inares Kenne Tsangue
- Organization: Youths4Change Initiative
- Academic Institution: Ashesi University
- Contact: inares.tsangue@ashesi.edu.gh

## 🔗 Links

- **Frontend Repository**: [youths4change-frontend](https://github.com/InaresKenne/youths4change-frontend)
- **Backend Repository**: [youths4change-backend](https://github.com/InaresKenne/youths4change-backend)
- **Live API**: https://youths4change-api.onrender.com
- **Live Website**: https://youths4change-frontend.vercel.app
- **Database**: Neon PostgreSQL (Serverless)

## 📝 License

MIT License - See LICENSE file for details

---

**Built with ❤️ by Youths4Change Initiative to empower young people across Africa**

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