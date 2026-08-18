# 🚀 AI-Powered Job Application Tracker

[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-orange.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive Django-based web application to manage and track job applications with AI-powered job description analysis.

## ✨ Features

### 🔐 User Authentication
- User Registration with validation
- Secure Login & Logout
- Profile Management
- User-specific data isolation

### 📝 Job Application Management
- **CRUD Operations**: Create, Read, Update, Delete applications
- **Status Tracking**: Wishlist → Applied → Screening → Interview → Selected/Rejected
- **Detailed Information**:
  - Job Title & Company Name
  - Job Description
  - Location & Salary
  - Job URL
  - Application Date
  - Notes
- **Categories & Tags** for better organization
- **Interview Management**:
  - Date & Time
  - Interview Type (Phone, Video, On-site, Technical, HR, Panel)
  - Meeting Link
  - Interview Notes

### 🔍 Search & Filtering
- Search by job title or company name
- Filter by status
- Filter by location
- Filter by category

### 🤖 AI Features
- **Job Description Analyzer** (OpenAI powered):
  - Auto-generate job summary
  - Extract required skills
  - Identify required experience
  - List important technologies
  - Generate interview preparation suggestions
- **Fallback Mode**: Works even without OpenAI API key

### 📊 Dashboard
- Total application count
- Applications by status (interactive chart)
- Recent applications list
- Upcoming interviews

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Backend | Django 4.2 |
| Frontend | Bootstrap 5, Chart.js |
| Database | SQLite (dev) / PostgreSQL (prod) |
| AI | OpenAI API (GPT-3.5-turbo) |
| Authentication | Django Auth System |
| Deployment | Heroku / PythonAnywhere |

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)



