# Floating Blood Donation System Backend

## Table of Contents
1. Introduction
2. Features
3. Requirements
4. Installation
5. Configuration
6. Usage
7. API Endpoints
8. Contributing
9. License


## Introduction
Welcome to the Floating Blood Donation System Backend repository! This Django-based backend is designed to support our blood donation organization's efforts. It provides essential features for managing donors, recipients, blood types, and appointments. This document will guide you through setting up and using the backend.

## Features
   * User Management: Registration, login, and profile management for donors, recipients, and administrators.
   * Donor Information: Collect and manage information about donors, including blood type and medical history.
   * Recipient Management: Track recipients in need of blood and manage their appointments.
   * Appointment Scheduling: Allow users to schedule appointments for blood donations.
   * Blood Type Matching: Find donors with compatible blood types for recipients.


## Requirements
Before getting started, make sure you have the following dependencies installed
   * Code editor (Visual studio code recommended) 
   * Python (3.1 +)
   * Django (3.6 +)
   * Virtual Environment (optional but recommended)
   * Other dependencies can be found in the requirements.txt file.

## Installation
1. Clone this repository to your local machine:
   * `git clone https://github.com/Jan-Briddhi-Foundation/bloodbankBackend.git`

2. Navigate to the project directory:
   * `cd blood-donation-backend`

3. Create and activate a virtual environment (optional but recommended):
   * `python -m venv venv`
   * `# For MacOs: source venv/bin/activate`
   * `# For Windows: venv\Scripts\activate`

5. Install project dependecies:
   `pip install -r requirements.txt`

6. Run project and check port:
   * Run command `python manage.py runserver`
   * Check url http://localhost:8000/

## Configuration
I havent done any configurations yet.
 * Use `admin` and `#Dot9047` for username and password

## Usage 
1. Access the Django admin panel by visiting http://localhost:8000/admin/ the superuser account created earlier.
2. Use the admin panel to manage users, donors, recipients, appointments, and other data.
3. To interact with the API, explore the available endpoints (documented below) or use tools like Postman.

## API Endpoints
# AUTHENTICATION ENDPOINTS

### 1. Login
- **Endpoint:** `/api/auth/token/` (POST)
- **Description:** User authentication endpoint.
- **Parameters:**
  - `email`
  - `password`
- **Response:** Returns an authentication token.

### 2. Logout
- **Endpoint:** `/api/auth/logout/` (POST)
- **Description:** User logout endpoint.
- **Parameters:** None
- **Response:** Logs out the user and invalidates the token.

### 3. User Registration
- **Endpoint:** `/api/auth/register/` (POST)
- **Description:** User registration endpoint.
- **Parameters:**
  - `email`
  - `email`
  - `password`
- **Response:** Confirms user registration.

### 4. Password Change
- **Endpoint:** `/api/auth/change-password/` (POST)
- **Description:** Password change endpoint.
- **Parameters:**
  - `old_password`
  - `new_password`
- **Response:** Confirms the password change.

### 5. Password Reset
- **Endpoint:** `/api/auth/reset-password/` (POST)
- **Description:** Password reset request endpoint.
- **Parameters:**
  - `email`
- **Response:** Sends an email with instructions to reset the password.

---

### 1. User Registration
- **Endpoint:** `/api/auth/users/` (POST)
- **Description:** User registration endpoint.
- **Required Parameters:**
  - `name`
  - `email`
  - `password`
- **Example:**
  ```json
  {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+123456789",
    "password": "password",
    "profile": {
      "bloodgroup": "A+",
      "language": "English",
      "country": "USA",
      "city": "New York",
      "address": "123 Main St",
      "profile_pic": "profile.jpg",
      "profile_type": "donor"
    }
  }
  
- **profile_types**
  - donor
  - patient

- **bloodgroups**
  -  A+
  -  A-
  -  B+
  -  B-'
  -  AB+
  -  AB-
  -  O+
  -  O-
- **Response:** Sends a confirmation email with an activation link.

### 2. User Activation
- **Endpoint:** `/api/auth/users/activate/` (POST)
- **Description:** User activation endpoint.
- **Parameters:**
  - `uid` (user id)
  - `token` (activation token)
- **Response:** Activates the user account.

### 3. User Details
- **Endpoint:** `/api/auth/users/me/` (GET, PUT, PATCH)
- **Description:** User details endpoint.
- **Parameters:** None (GET), User data (PUT, PATCH)
- **Response:** Retrieves or updates user details.

### 4. User Deletion
- **Endpoint:** `/api/auth/users/me/` (DELETE)
- **Description:** User deletion endpoint.
- **Parameters:** None
- **Response:** Deletes the user account.

### 5. Password Change
- **Endpoint:** `/api/auth/users/set_password/` (POST)
- **Description:** Password change endpoint.
- **Parameters:**
  - `new_password`
  - `re_new_password`
- **Response:** Confirms the password change.

### 6. Password Reset
- **Endpoint:** `/api/auth/users/reset_password/` (POST)
- **Description:** Password reset request endpoint.
- **Parameters:**
  - `email`
- **Response:** Sends an email with instructions to reset the password.


## Contributing
We welcome contributions to improve this blood donation system. If you'd like to contribute, please follow Contribution Guidelines.

## Lincense
This project is not licensed yet