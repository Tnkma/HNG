# HNG Premium Coding Challenge: Backend API Development

## Challenge: API Mastery

Build a scalable RESTFUL API system for task management that enables users to create, read, update, and delete (CRUD) tasks. Emphasizing error handling, authentication, and scalability.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)

## Prerequisites

- Python (version 5.1.2 or higher)
- Django
- Django REST Framework
- MySQL
- Redis
- Simple JWT

## Installation

1. Clone the repository:
    ```sh
    https://github.com/Tnkma/HNG.git
    ```
2. Navigate to the project directory:
    ```sh
    cd HNG
    ```
3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Environment Variables

Create a `.env` file in the root directory and add the following variables:

- DJANGO_SECRET_KEY=<your_django_secret_key>
- MYSQL_DATABASE=<your_database_name>
- MYSQL_USER=<your_database_user>
- MYSQL_PASSWORD=<your_database_password>
- MYSQL_HOST=<your_database_host>
- REDIS_URL=<your_redis_url>


## Usage

Run the development server:
```sh
python manage.py runserver

The server will run on http://localhost:8000.

API Documentation
Endpoints

POST /api/users/register/: Registers/creates a new User
POST /api/users/login/: Logs in a users
GET /api/users/:id/: Get a user by ID
PUT /api/users/:id/update/: Update a task by ID
POST /api/users/logout/: log out a user
DELETE /api/users/:id/: Delete a task by ID

GET /api/: Get all tasks
POST /api/tasks/search/: searches for a task based on ['title', 'description', 'status', 'createdBy', 'AssignedTo', 'dueDate']
POST /api/tasks/create_task/: Create a new task
GET /api/tasks/:id/: Get a task by ID
PUT /api/tasks/:id/update/: Update a task by ID
DELETE /api/tasks/:id/delete/: Delete a task by ID


Error Handling
The API includes comprehensive error handling for all endpoints, ensuring proper status codes and messages are returned.

Authentication
The API uses JWT for authentication. To access protected routes, include the following in the request headers:
Authorization: Bearer <token>

Contributing
Fork the repository
Create a new branch (git checkout -b feature/your-feature)
Commit your changes (git commit -m 'Add some feature')
Push to the branch (git push origin feature/your-feature)
Open a Pull Request
License
This project is licensed under the MIT License. See the LICENSE file for more details.

Contact Information
For any inquiries, please contact:

Name: Godswill Chimnonso
Email: onwusilikegodswill@gmail.com
