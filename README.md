# NC Voting Portal 🗳️

A secure, non complex web-based voting system designed for educational institutions specifically for Daeyang University to manage student representative council elections. This portal provides a complete solution for voter registration, candidate management, voting, and results automation and visualization.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [How to Use](#how-to-use)
- [User Roles](#user-roles)
- [Database](#database)
- [Security Features](#security-features)
- [Troubleshooting](#troubleshooting)

---

## 📖 Overview

The **NC Voting Portal** is a Django-based web application that manages the electoral process for Daeyang University student representative council election. It eliminates paper-based voting by providing a digital, transparent, non complex and secure voting platform.
The system is currently deployed on render.com free plan tier : https://nc-voting-portal.onrender.com/


**Target Users:**
- Students (Voters)
- Election Administrators
- Election Observers
- System Manager/developer

---

## ✨ Features

### For Students (Voters)
- **Secure Login**: Student ID + Voter ID authentication
- **Easy Voter Registration**: Quick registration to receive a Voter ID
- **Simple Voting Interface**: Clean, intuitive dashboard for casting votes
- **Multiple Positions**: Vote for different positions (e.g., President, Vice President, etc.)
- **Results Tracking**: View live voting results and statistics
- **Help Section**: Comprehensive guide on how to use the system

### For Administrators
- **Admin Dashboard**: Overview of voting system status
- **Candidate Management**: Add, edit, and approve candidates
- **Voter Management**: View registered voters and manage voter lists
- **Valid Student List**: Maintain the list of eligible voters
- **Voting Timer Control**: Set start/stop times for voting periods
- **Results & Reports**: View election results and voting statistics
- **Vote Clearing**: Reset votes (if needed for testing or re-voting)
- **Security**: Admin login with role-based access control

### System Features
- **Countdown Timer**: Visual countdown for voting period
- **Cloudinary Integration**: Cloud storage for candidate photos
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: Live vote counting and result updates
- **Brute Force Protection**: Security against unauthorized login attempts
- **Session Management**: Secure session handling and automatic logout

---

## 🖥️ System Requirements

Before you start, ensure your system has:

| Requirement | Version |
|---|---|
| **Python** | 3.8 or higher |
| **pip** | Latest version |
| **Git** | Latest version |
| **Browser** | Any modern browser (Chrome, Firefox, Safari, Edge) |
| **OS** | Windows, macOS, or Linux |

**Optional (for production):**
- PostgreSQL database
- Cloudinary account (for image hosting)

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd nc_voting_portal
```

### Step 2: Create a Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory and add:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Optional - defaults to SQLite)
# DATABASE_URL=postgresql://user:password@localhost:5432/voting_db

# Cloudinary (Optional - for image storage)
CLOUD_NAME=your-cloudinary-name
CLOUD_API_KEY=your-api-key
CLOUD_API_SECRET=your-api-secret
```

**Generate a secure SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Step 5: Apply Database Migrations

```bash
python manage.py migrate
```

### Step 6: Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your admin account:
- **Username**: Enter admin username
- **Email**: Enter admin email
- **Password**: Enter a strong password

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

---

## 📁 Project Structure

```
nc_voting_portal/
├── vote/                          # Main voting app
│   ├── models.py                  # Student, Voter, Candidate, Vote models
│   ├── views.py                   # Voting logic and dashboard views
│   ├── forms.py                   # Registration and voting forms
│   ├── urls.py                    # Voting app routes
│   ├── utils.py                   # Helper functions
│   ├── templates/vote/            # Student-facing pages
│   │   ├── home.html              # Homepage
│   │   ├── login.html             # Student login
│   │   ├── voter_register.html    # Voter registration
│   │   ├── dashboard.html         # Voting dashboard
│   │   ├── apply.html             # Candidate application
│   │   ├── results.html           # Results display
│   │   ├── help.html              # Help/FAQ page
│   │   └── about.html             # About page
│   └── static/vote/               # CSS, JS, images for voting app
│
├── customadmin/                   # Admin management app
│   ├── models.py                  # Admin-specific models
│   ├── views.py                   # Admin dashboard logic
│   ├── forms.py                   # Admin forms
│   ├── urls.py                    # Admin routes
│   ├── templates/customadmin/     # Admin pages
│   │   ├── login.html             # Admin login
│   │   ├── dashboard.html         # Admin dashboard
│   │   ├── manage_candidates.html # Manage candidates
│   │   ├── valid_students_list.html # View eligible voters
│   │   ├── registered_voters.html # View registered voters
│   │   └── results.html           # View results (admin view)
│   └── static/customadmin/        # CSS, JS for admin panel
│
├── ncportal/                      # Main project settings
│   ├── settings.py                # Django configuration
│   ├── urls.py                    # Main URL router
│   ├── wsgi.py                    # Production server config
│   └── asgi.py                    # Async server config
│
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── db.sqlite3                     # SQLite database (default)
└── README.md                      # This file
```

**What each app does:**

| App | Purpose |
|---|---|
| **vote** | Handles student voting, registration, results, and public-facing pages |
| **customadmin** | Handles administrative tasks and election management |
| **ncportal** | Main Django project configuration and settings |

---

## 🎯 How to Use

### For Students/Voters

#### 1. Register as a Voter
- Go to **Home** → **Register as Voter**
- Enter your **Student ID** (must be in the valid students list)
- Click **Register** to generate your **Voter ID**
- Save your Voter ID securely

#### 2. Login to Vote
- Go to **Home** → **Login**
- Enter your **Student ID** and **Voter ID**
- Click **Login**

#### 3. Apply for Candidate (if willing to be a candidate)
- log in
- Click on “Apply for Candidate” on the Voting Dashboard.
- Fill and submit the form.
- Wait for approval.



#### 4. Vote
- On the **Voting Dashboard**, you'll see all available positions
- Select your preferred candidate for each position
- Click **Vote** to confirm
- A confirmation message will appear

#### 5. View Results
- Go to **Results** to see live voting statistics
- View vote counts and percentages by position

### For Administrators

#### 1. Access Admin Panel
- Go to **Admin Login** (URL: `/admin/login/`)
- Enter your username and password
- You'll be redirected to the **Admin Dashboard**

#### 2. Manage Valid Students
- Go to **Admin Dashboard** → **Valid Students List**
- Add or remove eligible voters
- Upload CSV file for bulk import (if available)

#### 3. Manage Candidates
- Go to **Admin Dashboard** → **Manage Candidates**
- Approve or reject candidates
- delete candidates

#### 4. Control Voting Period
- Go to **Admin Dashboard** → **Countdown Timer Control**
- Set the start and end times for voting
- The timer will appear on the student dashboard

#### 5. View Results
- Go to **Admin Dashboard** → **Results**
- See detailed voting statistics
- Export results (if functionality available)

#### 6. Manage Security
- Go to **Admin Dashboard** → **Change Password**
- Update password whenever necessary

---

## 👥 User Roles

### Student/Voter
- **Permissions**: Register, vote, view results, apply for candidate
- **Restrictions**: Can only vote once per election
- **Access**: Student portal

### Administrator
- **Permissions**: Full system access
- **Responsibilities**: 
  - Manage voters and candidates
  - Control voting period
  - Monitor results
  - Ensure system security
- **Access**: Admin panel

### System Manager
- **Permissions**: Django superuser (full system access)
- **Responsibilities**: User management, system configuration and updates
- **Access**: Django admin interface

---

## 💾 Database

### Models Overview

**ValidStudent**
- Stores all eligible voters (students)
- Fields: Full Name, Student ID, Program, Year of Study, Status

**Voter**
- Records registered voters
- Fields: Voter ID, Voting Status (voted/not voted) 
- Linked to ValidStudent

**Candidate**
- Stores candidate information
- Fields: Name, Position, Program, Photo, manifesto, Approval Status

**Vote**
- Records each vote cast
- Fields: Voter ID, Candidate ID, Position, Timestamp

**CountdownTimer**
- Manages voting period times
- Fields: Start Time, End Time, Status

### Database Options

**Default (Development):**
```
SQLite (db.sqlite3) - default by Django and Suitable for testing and small-scale use
```

**Production:**
```
PostgreSQL - Recommended for production deployments
Set DATABASE_URL in .env to switch
```

---

## 🔒 Security Features

The system implements multiple security layers:

| Feature | Purpose |
|---|---|
| **CSRF Protection** | Prevents cross-site request forgery attacks |
| **Session Management** | Secure session rotation on login |
| **Brute Force Protection** | Limits login attempts via django-axes |
| **Password Hashing** | Argon2 hashing for password security |
| **HTTPS Ready** | Configured for SSL/TLS in production |
| **Authentication** | Role-based access control |
| **Input Validation** | Server-side form validation |
| **Secure Headers** | Security middleware enabled |

### Best Practices

1. **Change Default SECRET_KEY** in `.env` before deployment
2. **Use Strong Passwords** for admin accounts
3. **Enable HTTPS** in production
4. **Regular Backups** of the database
5. **Monitor Logs** for suspicious activities
6. **Keep Dependencies Updated** regularly

---

## 🐛 Troubleshooting

### Common Issues & Solutions

**Issue**: "No such table" error when running the server
```bash
# Solution: Run migrations
python manage.py migrate
```

**Issue**: "ModuleNotFoundError" when starting the server
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt
```

**Issue**: Static files not loading (CSS/JS not working)
```bash
# Solution: Collect static files
python manage.py collectstatic --noinput
```

**Issue**: Cannot login with admin account
```bash
# Solution: Reset the superuser password
python manage.py changepassword <username>
```

**Issue**: Images not uploading or displaying
```bash
# Check Cloudinary credentials in .env
# Verify CLOUD_NAME, CLOUD_API_KEY, CLOUD_API_SECRET
```

**Issue**: Port 8000 already in use
```bash
# Solution: Use a different port
python manage.py runserver 8001
```

**Issue**: Virtual environment not activating
```bash
# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

---

## 📝 Environment Variables Reference

| Variable | Example | Required | Purpose |
|---|---|---|---|
| `SECRET_KEY` | `django-insecure-...` | Yes | Django security key |
| `DEBUG` | `True` or `False` | No | Debug mode (default: True) |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | No | Allowed domain list |
| `DATABASE_URL` | `postgresql://...` | No | Database connection string |
| `CLOUD_NAME` | `your-cloud` | No | Cloudinary cloud name |
| `CLOUD_API_KEY` | `123456789` | No | Cloudinary API key |
| `CLOUD_API_SECRET` | `secret123` | No | Cloudinary secret |

---

## 🚀 Deployment (Production)

### Steps to Deploy

1. **Use PostgreSQL database** instead of SQLite
2. **Set DEBUG = False** in `.env`
3. **Configure ALLOWED_HOSTS** with your domain
4. **Collect static files**: `python manage.py collectstatic`
5. **Use a production server** like Gunicorn:
   ```bash
   gunicorn ncportal.wsgi:application
   ```
6. **Enable HTTPS** with an SSL certificate
7. **Use environment variables** for sensitive data

### Recommended Hosting Platforms
- Render
- Heroku
- AWS
- DigitalOcean
- PythonAnywhere

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Python Documentation](https://docs.python.org/)
- [Cloudinary Documentation](https://cloudinary.com/documentation)
- [WhiteNoise (Static Files)](http://whitenoise.evans.io/)

---

## 📧 Support

For issues, questions, or feature requests, please contact the developer or open an issue in the repository.

---

## 📄 License

This project is provided as-is for educational and institutional use.

---

## 👨‍💻 Developer

Created and maintained for **Gracious K Banda**.

---

**Last Updated**: June 2026  
**Version**: 1.0.0
