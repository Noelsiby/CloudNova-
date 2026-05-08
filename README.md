Nova Events 2026 – Cloud-Based Event Booking System

A full-stack cloud-native event booking and management platform deployed using AWS services.
The system allows users to browse events, book seats, generate QR-based tickets, and enables administrators to manage events dynamically through a dedicated admin dashboard.

Project Overview

Nova Events 2026 is designed as a cloud-hosted event management solution that demonstrates real-world deployment using AWS infrastructure.

The project includes:

User Authentication System
Dynamic Event Management
Event Booking System
QR Code Ticket Generation
Admin Dashboard
Cloud Deployment using AWS
Features
User Features
User Registration
User Login Authentication
Browse Available Events
View Dynamic Event Details
Book Event Seats
Generate Unique Ticket IDs
QR Code Ticket Generation
View Booking History
Admin Features
Admin Authentication
Create Multiple Events
Manage Event Listings
View Booking Statistics
View User Bookings
Track Available Seats
AWS Cloud Architecture

The application follows a cloud-based architecture using AWS services.

AWS Services Used
AWS Service	Purpose
Amazon S3	Static frontend hosting
Amazon EC2	Flask backend hosting
Amazon RDS	MySQL database hosting
IAM	Secure access management
Security Groups	Firewall & traffic control
Architecture Flow
User Browser
     ↓
Amazon S3 (Frontend Hosting)
     ↓
Flask Backend API (EC2)
     ↓
Amazon RDS (MySQL Database)
Technology Stack
Frontend
HTML5
CSS3
JavaScript
Backend
Python
Flask
Database
MySQL (Amazon RDS)
Cloud Platform
AWS EC2
AWS S3
AWS RDS
Additional Libraries
qrcode
PyMySQL
Flask-CORS
Project Structure
NovaEvents2026/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── routes/
│   ├── static/
│   └── requirements.txt
│
├── frontend/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── event_details.html
│   ├── my_bookings.html
│   ├── booking_confirmation.html
│   ├── admin_dashboard.html
│   ├── css/
│   └── js/
│
└── README.md
Database Tables
Users Table

Stores:

User ID
Name
Email
Password
Role
Events Table

Stores:

Event ID
Event Title
Description
Event Date
Location
Total Seats
Available Seats
Bookings Table

Stores:

Booking ID
User ID
Event ID
Ticket ID
Booking Status
Setup Instructions
1. Clone Repository
git clone https://github.com/yourusername/nova-events-2026.git
cd nova-events-2026
2. Create Virtual Environment
python -m venv venv

Activate virtual environment:

Windows
venv\Scripts\activate
Linux / Mac
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure Database

Update database configuration in:

database.py

Example:

host = "your-rds-endpoint"
user = "admin"
password = "password"
database = "novaevents"
5. Run Flask Backend
python app.py

Backend runs on:

http://localhost:5000
6. Configure Frontend API URL

Update API base URL in:

js/main.js

Example:

const API_BASE_URL = "http://your-ec2-public-ip:5000";
AWS Deployment Steps
Frontend Deployment
Create S3 Bucket
Enable Static Website Hosting
Upload frontend files
Configure bucket policy
Backend Deployment
Launch EC2 Instance
Install Python & Flask
Upload backend files
Configure Security Groups
Run Flask server
Database Deployment
Create Amazon RDS MySQL instance
Configure inbound rules
Connect Flask backend to RDS
Security Features
Session-Based Authentication
Role-Based Access Control
Secure API Access
IAM Permission Management
Security Group Firewall Rules
Challenges Faced
Dynamic event routing
Multiple event handling
EC2 public IP management
Frontend-backend API integration
AWS permission configuration
Security Group setup
Future Enhancements
CloudFront CDN Integration
HTTPS with Route 53
Email Notifications using SES
CI/CD with CodePipeline
Payment Gateway Integration
Mobile App Support
CloudWatch Monitoring
Screenshots
User Dashboard

(Add screenshot here)

Event Details Page

(Add screenshot here)

Admin Dashboard

(Add screenshot here)

Booking Confirmation

(Add screenshot here)

Learning Outcomes

This project helped in understanding:

AWS Cloud Deployment
Full-Stack Application Development
REST API Integration
Database Management
Cloud Security Concepts
Real-world Cloud Architecture
References
AWS Documentation
https://aws.amazon.com/documentation/
Flask Documentation
https://flask.palletsprojects.com/
MySQL Documentation
https://dev.mysql.com/doc/
Author
Nova Events 2026 Project

Developed as an academic cloud computing project demonstrating AWS cloud deployment and full-stack application development.

License

This project is created for educational and academic purposes.
