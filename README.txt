# Secure 2FA Forum System

> A high-security web application combining a community forum with a custom-built Two-Factor Authentication (2FA) system compliant with RFC 6238 standards.

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Django](https://img.shields.io/badge/django-5.x-green.svg)
![Security](https://img.shields.io/badge/security-TOTP%2F2FA-red.svg)

##  Author

**Chau Nhat Hoa - gachipper ** *Full-stack Developer & Security Engineer* 

---

##  Overview

This project is a comprehensive **Forum Platform** engineered with a "Security First" mindset. Unlike standard implementations that rely solely on third-party libraries, the core security modules—specifically the **Time-based One-Time Password (TOTP)** algorithm—were implemented from scratch to demonstrate deep understanding of cryptographic standards.

The system features a robust **Role-Based Access Control (RBAC)** model, real-time security monitoring, and high-performance rate limiting using Redis, making it suitable for enterprise-grade deployment.

##  Key Features

### Advanced Security & Authentication
* **Custom TOTP Implementation**: Built the TOTP/HOTP algorithm from scratch following **RFC 6238** and **RFC 4226** standards (SHA-1/SHA-256 HMAC), compatible with Google Authenticator/Authy.
* **Multi-Layered 2FA**:
    * **App-based**: QR Code generation for authenticator apps.
    * **Email-based**: Fallback OTP delivery via SMTP.
    * **Backup Codes**: Generation of hashed one-time recovery codes.
* **Adaptive Rate Limiting**: Integrated **Redis** to prevent Brute-force and Dictionary attacks on login/OTP endpoints.
* **Account Lockout Policies**: Automatic temporary locking after excessive failed attempts.
* **Session Security**: Device trust management ("Remember this device") and remote session revocation (Force logout from all devices).

### Admin Security Dashboard
* **Real-time Monitoring**: Visual dashboard tracking failed login attempts, 2FA adoption rates, and suspicious IP activities.
* **RBAC Enforcement**: Granular permission settings allowing Admins to enforce 2FA policies for specific user groups (e.g., mandatory 2FA for Staff).
* **Audit Logging**: Comprehensive logging of all security-critical events (Login, OTP Fail, Password Change) with User-Agent and IP tracking.

### Community Forum
* **Thread Management**: Create, read, update, and delete (CRUD) threads and posts.
* **Rich Interaction**: Reply system with pagination, like/unlike functionality using AJAX.
* **Moderation Tools**: Staff can lock/unlock threads to prevent further discussion.
* **User Profiles**: Customizable avatars, bio, and activity history.

## Tech Stack

### Backend
* **Framework**: Python Django 5.x
* **Database**: MySQL (Production) / SQLite (Dev)
* **Caching & Throttling**: Redis (django-redis, django-ratelimit)
* **Cryptography**: `cryptography` library for Fernet encryption (securing OTP secrets in DB).

### Frontend
* **Templates**: Django Template Engine (DTL)
* **Styling**: Custom CSS (Material Design inspired), Responsive Layout.
* **Scripting**: Vanilla JavaScript (AJAX, Chart.js for Dashboard).

### Infrastructure (DevOps)
* **Server**: AWS EC2 (Ubuntu Linux)
* **Web Server**: Nginx as Reverse Proxy
* **WSGI**: Gunicorn
* **Environment**: Python `venv`, Environment Variables (`.env`) for secrets management.

## Installation & Setup

### Prerequisites
* Python 3.10+
* MySQL Server
* Redis Server

### Steps

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/twofa_site.git](https://github.com/yourusername/twofa_site.git)
    cd twofa_site
    ```

2.  **Set up Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/macOS
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**
    Create a `.env` file in the root directory:
    ```env
    DEBUG=True
    SECRET_KEY=your-secret-key
    DB_NAME=db_name
    DB_USER=user
    DB_PASS=pass
    OTP_ENCRYPTION_KEY=generated-fernet-key
    ```

5.  **Database Migration**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Run Development Server**
    ```bash
    python manage.py runserver
    ```

## 📸 Screenshots

*(Add screenshots of your Security Dashboard, 2FA Setup Screen, and Forum Home here)*

## 📄 License

This project is created by **Chau Nhat Hoa - gachipper **. All rights reserved.
