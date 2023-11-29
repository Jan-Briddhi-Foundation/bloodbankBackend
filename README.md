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
   * `cd bloodbankBackend`

3. Create and activate a virtual environment (optional but recommended):
   * `python -m venv venv`
   * `# For MacOs: source venv/bin/activate`
   * `# For Windows: venv\Scripts\activate`

5. Install project dependecies:
   `pip install -r requirements.txt` or `python -m pip install -r requirements.txt`

6. Run project and check port:
   * Run command `python manage.py runserver`
   * Check url http://localhost:8000/

## Configuration
I havent done any configurations yet.
 * Use `admin@gmail.com` and `#Dot9047` for email and password

## Usage 
1. Access the Django admin panel by visiting http://localhost:8000/admin/ the superuser account created earlier.
2. Use the admin panel to manage users, donors, recipients, appointments, and other data.
3. To interact with the API, explore the available endpoints (documented below) or use tools like Postman.

## API Endpoints

## i.) Authenication Endpoints

### 1. Login
- **Endpoint:** `/api/auth/login/` (POST)
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
  - `name`
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
      "bloodGroup": "A+",
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

- **bloodGroups**
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


---


## ii.) Social Authenication Endpoints

### 1. Facebook
- **Endpoint:** `/api/auth/facebook/` (POST)
- **Description:** Authenticate users via Facebook
- **Parameters:** None (GET), User data (PUT, PATCH)
- **Response:** Returns an authentication token.

### 2. Twitter
- **Endpoint:** `/api/auth/twitter/` (POST)
- **Description:** Authenticate users via Twitter
- **Parameters:** None (GET), User data (PUT, PATCH)
- **Response:** Returns an authentication token.

### 3. Google
- **Endpoint:** `/api/auth/google/` (POST)
- **Description:** Authenticate users via Google
- **Parameters:** None (GET), User data (PUT, PATCH)
- **Response:** Returns an authentication token.

---


## iii.) Home Endpoints

### 1. Home Page
- **Endpoint:** `/api/home/` (GET)
- **Description:** Retrieves user's home page details.
- **Permissions:** User must be authenticated.
  
#### Response
- **Success (200 OK):**
    - Returns user's home page details.
        - For donors: Redirects to 'donor_home'.
        - For patients: Redirects to 'patient_home'.
        - For other profiles: Redirects to 'user_details'.
- **User Details Update (200 OK):**
    - If user's profile doesn't exist, creates a profile, updates user details, and returns a success message.


### 2. User Details
- **Endpoint:** `/api/personal-details/` (POST)
- **Description:** Updates user's personal details.
- **Permissions:** User must be authenticated.

#### Request
- **Method:** POST
- **Parameters:** User details in the request body.

#### Response
- **Success (200 OK):**
    - Returns a success message if user details are updated successfully.

- **Bad Request (400):**
    - Returns validation errors if the provided data is invalid.


### 3. Donor Home
- **Endpoint:** `/api/donor-home/` (GET)
- **Description:** Retrieves blood donation requests for donors.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns a list of blood donation requests.


### 4. Donation Criteria
- **Endpoint:** `/api/donation-criteria/` (POST)
- **Description:** Validates and processes user's donation criteria form.
- **Permissions:** User must be authenticated.

#### Request
- **Method:** POST
- **Parameters:** Donation criteria form data in the request body.

#### Response
- **Success (200 OK):**
    - Returns a success message if the user is eligible for donation.

- **Bad Request (400):**
    - Returns a message indicating ineligibility if the criteria are not met

### 5. Location Map
- **Endpoint:** `/api/location-map/` (GET)
- **Description:** Retrieves and renders the location map.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns a message indicating the rendering of the location map.

### 6. Not Eligible
- **Endpoint:** `/api/not-eligible/` (GET)
- **Description:** Notifies the user of ineligibility.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns a message indicating user ineligibility.
    

### 7. Hospital Address
- **Endpoint:** `/api/hospital-address/` (POST)
- **Description:** Adds a hospital address.
- **Permissions:** User must be authenticated.

#### Request
- **Method:** POST
- **Parameters:** Hospital address data in the request body.

#### Response
- **Success (200 OK):**
    - Returns a success message if the hospital is added successfully.

- **Bad Request (400):**
    - Returns validation errors if the provided data is invalid.


### 8. Donation Agreement
- **Endpoint:** `/api/donation-agreement/` 
    - **GET:** Retrieves user's donation agreement form.
    - **POST:** Submits a donation agreement request.
- **Description:** Allows users to view and submit donation agreements.
- **Permissions:** User must be authenticated.

#### GET Request
- **Response (200 OK):**
    - Returns user's donation agreement form.

#### POST Request
- **Request:**
    - Donation agreement data in the request body.
- **Response:**
    - Returns a success message if the donation agreement is sent successfully.
    - Returns an error message if the provided data is invalid.


### 9. Patient Home
- **Endpoint:** `/api/patient-home/` (GET)
- **Description:** Retrieves the patient's home page.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns a message indicating the patient's home page.

### 10. Profile
- **Endpoint:** `/api/profile/` (GET)
- **Description:** Retrieves the user's profile information.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns the user's profile information.

### 11. Edit Profile
- **Endpoint:** `/api/edit-profile/` 
    - **GET:** Retrieves user's edit profile forms.
    - **POST:** Updates user's profile information.
- **Description:** Allows users to view and edit their profile details.
- **Permissions:** User must be authenticated.

#### GET Request
- **Response (200 OK):**
    - Returns user's edit profile forms.

#### POST Request
- **Request:**
    - User data and profile data in the request body.
- **Response:**
    - Returns a success message if the profile is updated successfully.
    - Returns an error message if the provided data is invalid.

### 12. Request Blood
- **Endpoint:** `/api/request-blood/` 
    - **GET:** Retrieves user's blood request form.
    - **POST:** Submits a blood request.
- **Description:** Allows users to request blood donations.
- **Permissions:** User must be authenticated.

#### GET Request
- **Response (200 OK):**
    - Returns user's blood request form.

#### POST Request
- **Request:**
    - Blood request data in the request body.
- **Response:**
    - Returns a success message if the blood request is sent successfully.
    - Returns an error message if the provided data is invalid.

### 13. Request Sent
- **Endpoint:** `/api/request-sent/` (GET)
- **Description:** Notifies the user of a successful blood request submission.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns a message indicating successful blood request submission.

### 14. Patient History
- **Endpoint:** `/api/patient-history/` (GET)
- **Description:** Retrieves the blood donation history for the patient.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns a list of blood donation history for the patient.

### 15. Delete Page
- **Endpoint:** `/api/delete-page/<int:pk>/` 
    - **GET:** Retrieves the item to be deleted.
    - **POST:** Deletes the specified item.
- **Description:** Allows users to view and delete specific items.
- **Permissions:** User must be authenticated.

#### GET Request
- **Response (200 OK):**
    - Returns the item to be deleted.

#### POST Request
- **Response (200 OK):**
    - Returns a success message if the item is deleted successfully.

### 16. Notifications
- **Endpoint:** `/api/notifications/` (GET)
- **Description:** Retrieves and renders the notifications page.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns a message indicating the rendering of the notifications page.

### 16. Blood Match Success
- **Endpoint:** `/api/blood-match-success/` (GET)
- **Description:** Retrieves and renders the blood match success page.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns a message indicating the rendering of the blood match success page

### 18. Error 404
- **Endpoint:** `/api/error404/` (GET)
- **Description:** Retrieves and renders the error 404 page.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns a message indicating the rendering of the error 404 page.


## Contributing
We welcome contributions to improve this blood donation system. If you'd like to contribute, please follow Contribution Guidelines.

## Lincense
This project is not licensed yet
