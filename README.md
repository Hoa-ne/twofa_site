#  Secure 2FA Forum Platform

<div align="center">

![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Security](https://img.shields.io/badge/Security-RFC_6238_TOTP-E63946?style=for-the-badge&logo=auth0&logoColor=white)


**A production-grade forum application with enterprise-level Two-Factor Authentication (2FA) and custom cybersecurity-themed UI.**

</div>

---



##  About This Project

A comprehensive forum platform built with a "security-first" approach. Instead of using third-party libraries for authentication, I implemented the **TOTP (Time-based One-Time Password)** algorithm **from scratch** following **RFC 6238** and **RFC 4226** standards.

The project also features a modern, responsive UI with a cybersecurity theme designed for optimal user experience.





###  Frontend & User Interface

**Cybersecurity-Themed Dark Mode**
- Deep blue/grey color palette with neon accents
- High-contrast typography for readability
- Designed for long reading sessions

**Modern UI Effects**
- Glassmorphism with `backdrop-filter` and semi-transparent cards
- Smooth animations and hover effects
- Professional gradient backgrounds

**Responsive Design**
- Mobile-first architecture using Flexbox & CSS Grid
- Perfect rendering on iPhone, iPad, and Desktop
- Touch-optimized for mobile devices

**Interactive Dashboard**
- Real-time security metrics with Chart.js
- Attack vector visualization
- Login attempt tracking

**Dynamic User Experience**
- AJAX-powered interactions (no page reloads)
- Instant form validation
- Real-time like/unlike functionality

###  Security & Authentication

**Custom TOTP Implementation**
- Built from scratch following RFC 6238/4226
- Compatible with Google Authenticator and Authy
- SHA-1/SHA-256 HMAC-based algorithm

**Multi-Factor Authentication**
- **QR Code Setup** – Scan with authenticator apps
- **Email OTP** – Fallback delivery via SMTP
- **Backup Codes** – 10 one-time recovery codes (hashed)

**Attack Prevention**
- **Rate Limiting** – Redis-powered IP throttling
- **Account Lockout** – Auto-lock after failed attempts
- **Session Security** – Device trust management
- **Encrypted Storage** – Fernet encryption for OTP secrets

**Admin Monitoring**
- Real-time security dashboard
- Failed login attempt tracking
- 2FA adoption statistics
- Audit logging with IP and User-Agent

###  Forum Features

**Content Management**
- Create, read, update, delete threads and posts
- Rich text formatting support
- User profiles with avatars and bio

**Social Interactions**
- Reply to threads with pagination
- Like/unlike posts
- User activity history

**Moderation Tools**
- Lock/unlock threads (Staff only)
- Delete inappropriate content
- Role-based permissions (Admin/Staff/User)

---

##  Tech Stack

<table>
<tr>
<td valign="top" width="33%">

### Frontend
- HTML5, CSS3
- Vanilla JavaScript (ES6+)
- Chart.js for analytics
- FontAwesome icons
- BEM CSS methodology

</td>
<td valign="top" width="33%">

### Backend
- Django 5.x
- Python 3.10+
- MySQL database
- Redis caching
- Custom cryptography

</td>
<td valign="top" width="33%">

### Infrastructure
- AWS EC2 (Ubuntu)
- Nginx reverse proxy
- Gunicorn WSGI
- Systemd process manager
- Python venv

</td>
</tr>
</table>

---

##  Project Structure

```
twofa_site/
├── accounts/              # Authentication & Security
│   ├── otp_algo.py       # Custom TOTP implementation
│   ├── models.py         # User, SecurityLog, BackupCode
│   ├── views.py          # Login, Register, OTP views
│   └── admin.py          # Admin panel customizations
├── forum/                # Community Forum
│   ├── models.py         # Thread, Post, Category
│   └── views.py          # Forum CRUD operations
├── static/               # Frontend Assets
│   ├── css/app.css       # Main stylesheet
│   └── js/app.js         # JavaScript logic
├── templates/            # HTML templates
├── manage.py
└── requirements.txt
```

---

##  Installation

### Prerequisites
- Python 3.10+
- MySQL Server
- Redis Server

### Quick Start

```bash
# Clone repository
git clone https://github.com/gachipper/twofa_site.git
cd twofa_site

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Create .env file with:
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=twofa_db
DB_USER=your-username
DB_PASS=your-password
OTP_ENCRYPTION_KEY=your-fernet-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Setup database
python manage.py makemigrations
python manage.py migrate

# Create admin account
python manage.py createsuperuser

# Run development server
python manage.py runserver
```





##  License

This project is created by **Chau Nhat Hoa - gachipper **
All rights reserved.

contact: chaunhathoa24102004@gmail.com

---

<div align="center">


⭐ Star this repository if you find it useful!

</div>
