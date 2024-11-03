# incident_management_system
Here is the incident management system. where a a users can create, edit and view the incident reported by them and others


Incident Management System - Backend
The Incident Management System is developed using Python and Django Rest Framework (DRF). This system allows users to manage and report incidents with various details and functionalities.

Features
User registration and authentication.
User profile with details such as name, email, phone number, address, city, and country.
Create, view, edit, and delete incidents.
Each incident includes information about the reporter, details, date and time of reporting, priority, and status.
Auto-generation of unique incident IDs.
Search incidents by Incident ID.
Control over incident editing:
Users can only edit their own incidents.
Closed incidents are not editable.
Installation
Clone the repository to your local machine: git clone

Change into the project directory: cd incident-management-system

Install project dependencies: pip install -r requirements.txt

Set up the database: python manage.py migrate

Create a superuser (admin) account: python manage.py createsuperuser

Start the development server: python manage.py runserver

Access the application at http://localhost:8000/.

API Endpoints
User Registration
POST /api/users/register/: Register a new user.

User Management
GET /api/users/: List all users.
GET /api/users/?user_id=<user_id>: Retrieve a specific user by ID.
PUT /api/users/update/?user_id=<user_id>: Update a specific user by ID.
DELETE /api/users/delete/?user_id=<user_id>: Delete a specific user by ID.
Incident Management
POST /api/incidents/: Create a new incident.
GET /api/incidents/: List all incidents created by the logged-in user.
GET /api/incidents/?incidentid=<incident_id>: Retrieve a specific incident by ID.
PUT /api/incidents/?incidentid=<incident_id>: Update a specific incident by ID (if not closed).
DELETE /api/incidents/?incidentid=<incident_id>: Delete a specific incident by ID (if not closed).
Get Information from Pin Code
GET /api/pincode//: Retrieve information (City and Country) based on the entered PIN code.
