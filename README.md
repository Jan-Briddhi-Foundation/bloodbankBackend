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
   * Run command `python manage.py migrate`
   * Run command `python manage.py runserver`
   * Check url http://localhost:8000/

## Configuration
I havent done any configurations yet.
 * Use `admin@gmail.com` and `#Dot9047` for email and password

## Usage 
1. Access the Django admin panel by visiting http://localhost:8000/admin/ the superuser account created earlier.
2. Use the admin panel to manage users, donors, recipients, appointments, and other data.
3. To interact with the API, explore the available endpoints (documented below) or use tools like Postman.

<!-- 
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

<!--  -->
<!-- DON’T Make These 5 Coding Mistakes… -->
<!-- 5 IMPRESSIVE Python Resume Projects (You Can Finish in A Weekend) -->
<!-- I tried 50 Programming Courses. Here are Top 5. -->


-->
## API Endpoints

## i.) Authenication Endpoints

---

### 1. User Registration
- **Endpoint:** `/api/auth/users/` (POST)

- **Description:** User registration endpoint.
- **Required Parameters:**
  - `name`
  - `email`
  - `phone `
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


### 2. Login
- **Endpoint:** `/api/auth/login/` (POST)
- **Description:** User authentication endpoint.
- **Parameters:**
  - `email`
  - `password`
- **Response:** Returns an authentication token.


### 3. Logout
- **Endpoint:** `/api/auth/logout/` (POST)
- **Description:** User logout endpoint.
- **Parameters:** None
- **Response:** Logs out the user and invalidates the token.


<!-- 
### 4. User Activation
- **Endpoint:** `/api/auth/users/activation/` (POST)
- **Description:** User activation endpoint.
- **Parameters:**
  - `uid` (user id)
  - `token` (activation token)
- **Response:** Activates the user account. -->

<!-- 
### 5. User Details
- **Endpoint:** `/api/auth/users/me/` (GET, PUT, PATCH)
- **Description:** User details endpoint.
- **Parameters:** None (GET) 
- **Parameters:** (PUT, PATCH) User data
  - `email`
  - `name`
- **Response:** Retrieves or updates user details. -->

### 6. User Deletion
- **Endpoint:** `/api/auth/users/me/` (DELETE)
- **Description:** User deletion endpoint.
- **Parameters:** 
  - `current_password`
- **Response:** Deletes the user account.

### 7. Password Change
- **Endpoint:** `/api/auth/users/set_password/` (POST)
- **Description:** Password change endpoint.
- **Parameters:**
  - `current_password`
  - `new_password`
  - `re_new_password`
- **Response:** Confirms the password change.

### 8. Password Reset
- **Endpoint:** `/api/auth/users/reset_password/` (POST)
- **Description:** Password reset request endpoint.
- **Parameters:**
  - `email`
- **Response:** Sends an email with instructions to reset the password.


---


## ii.) Social Authenication Endpoints

### 1. Google
- **Endpoint:** `/social_auth/google/` (POST)
- **Description:** Authenticate users via Google
- **Parameters:** 
    - `auth_token`
- **Response:** Returns an authenicated user details, username, email and adds them in our database.

### 2. Facebook
- **Endpoint:** `/social_auth/facebook/` (POST)
- **Description:** Authenticate users via Facebook
- **Parameters:** 
    - `auth_token`
- **Response:** Returns an authenicated user details, username, email and adds them in our database.

### 3. Twitter
- **Endpoint:** `/social_auth/twitter/` (POST)
- **Description:** Authenticate users via Twitter
- **Parameters:** 
    - `access_token_key`
    - `access_token_secret`
- **Response:** Returns an authenicated user details, username, email and adds them in our database.



---


## iii.) Other Endpoints

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

### 2. Profile Details
- **Endpoint:** `/api/profile-details/` (POST)
- **Description:** Updates user's profile details.
- **Permissions:** User must be authenticated.

    #### Request
    - **Method:** POST
    - **Parameters:** 
        - `city`
        - `country`
        - `bloodGroup`
        - `profile_type`

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
    - **Parameters:** 
        - `qualify` (Boolean Value)

    #### Response
    - **Success (200 OK):**
        - Returns a success message if the user is eligible or NOT for donation.

    - **Bad Request (400):**
        - Returns validation errors if the provided data is invalid.

 ### 5. Donation Criteria Questions
- **Endpoint:** `/api/questions/` (POST)
- **Description:** For adding and retriving questions donation criteria form.
- **Permissions:** User must be authenticated.

    #### Request
    - **Method:** POST
    - **Parameters:** 
        - `question`
    - **Permissions:** User must be an admin.

    #### GET Request
    - **Response (200 OK):**
    - Returns all questions donation criteria form.


    #### Response
    - **Success (200 OK):**
        - Returns a success message if the user is eligible or NOT for donation.

    - **Bad Request (400):**
        - Returns validation errors if the provided data is invalid.

### 6. Donation Question Deletion
- **Endpoint:** `/api/questions/<int:question_id>/` (DELETE)
- **Description:** Donation Criteria question deletion endpoint.
- **Parameters:** None
- **Response:** Deletes the donation criteria question.


### 7. Donation Question Modification
- **Endpoint:** `/api/questions/<int:question_id>/` (PUT)
- **Description:** Donation Criteria question update endpoint.
- **Parameters:** None
- **Response:** Modifies the donation criteria question.
<!-- 

### 5. Location Map
- **Endpoint:** `/api/location-map/` (GET)
- **Description:** Retrieves and renders the location map.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns a message indicating the rendering of the location map. -->

<!-- ### 6. Not Eligible
- **Endpoint:** `/api/not-eligible/` (GET)
- **Description:** Notifies the user of ineligibility.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns a message indicating user ineligibility.
    
-->


### 8. Hospital Address
- **Endpoint:** `/api/hospital-address/` (POST)
- **Description:** Adds a hospital address.
- **Permissions:** User must be authenticated.

    #### Request
    - **Method:** POST
    - **Parameters:** 
        - `name`
        - `address`

    #### Response
    - **Success (200 OK):**
        - Returns a success message if the hospital is added successfully.

    - **Bad Request (400):**
        - Returns validation errors if the provided data is invalid.



 ### 9. Donation Agreement
- **Endpoint:** `/api/donation-agreement/` (POST, GET)
    - **GET:** Retrieves user's donation agreement forms.
    - **POST:** Submits a donation agreement request.
- **Description:** Allows users to view and submit donation agreements.
- **Permissions:** User must be authenticated.

    #### GET Request
    - **Response (200 OK):**
        - Returns user's donation agreement forms.

    #### POST Request
    - **Request:**
        - Donation agreement data in the request body.
    - **Parameters:** 
        - `hospital_address`
    - **Response:**
        - Returns a success message if the donation agreement is sent successfully.
        - Returns an error message if the provided data is invalid.

<!-- ### 9. Patient Home
- **Endpoint:** `/api/patient-home/` (GET)
- **Description:** Retrieves the patient's home page.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns a message indicating the patient's home page. -->

<!-- ### 10. Profile
- **Endpoint:** `/api/profile/` (GET)
- **Description:** Retrieves the user's profile information.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns the user's profile information. -->

### 10. Profile
- **Endpoint:** `/api/profile/` (POST, GET)
    - **GET:** Retrieves user's profile info.
    - **POST:** Updates user's profile info.
- **Description:** Allows users to view and edit their profile details.
- **Permissions:** User must be authenticated.

    #### GET Request
    - **Response (200 OK):**
        - Returns user's profile.

    #### POST Request
    - **Request:**
        - User and profile data in the request body.
    - **Response:**
        - Returns a success message if the profile is updated successfully.
        - Returns an error message if the provided data is invalid.
    - **Parameters:**
        - `name`
        - `email`
        - `phone`
        - `bloodGroup`
        - `langauge`
        - `country`
        - `city`
        - `address`
        - `profile_pic`

 ### 11. Request Blood
- **Endpoint:** `/api/request-blood/` (POST)
    - **POST:** Submits a blood request.
- **Description:** Allows users to request blood donations.
- **Permissions:** User must be authenticated.

    #### POST Request
    - **Request:**
        - Blood request data in the request body.
    - **Response:**
        - Returns a success message if the blood request is sent successfully.
        - Returns an error message if the provided data is invalid.
    - **Parameters:**
        - `quantity`
        - `date_needed`
<!-- 
### 13. Request Sent
- **Endpoint:** `/api/request-sent/` (GET)
- **Description:** Notifies the user of a successful blood request submission.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns a message indicating successful blood request submission. 
-->

### 12. Patient's Request History
- **Endpoint:** `/api/patient-history/` (GET)
- **Description:** Retrieves the blood donation history for the patient and provides the User's profile info.
- **Permissions:** User must be authenticated.

    #### Response
    - **Success (200 OK):**
        - Returns a list of blood donation history for the patient.
        - Returns User's profile information.


 ### 13. Notifications
- **Endpoint:** `/api/notifications/` (GET)
- **Description:** Retrieves requests for donors and or patients.
- **Permissions:** User must be authenticated.

    #### Response
    - **Success (200 OK):**
        - Returns a list of requests, use the `date_created` to create notifications.

<!-- ### 15. Delete Page
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
    - Returns a success message if the item is deleted successfully. -->

<!-- 
### 16. Notifications
- **Endpoint:** `/api/notifications/` (GET)
- **Description:** Retrieves and renders the notifications page.
- **Permissions:** User must be authenticated.

#### Response
- **Success (200 OK):**
    - Returns a message indicating the rendering of the notifications page. -->

<!-- ### 16. Blood Match Success
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

-->
## Contributing
We welcome contributions to improve this blood donation system. If you'd like to contribute, please follow Contribution Guidelines.

## Lincense
This project is not licensed yet
