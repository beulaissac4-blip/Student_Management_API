
# Student Management API

## Project Description
The Student Management API is a Python-based REST API application used to manage student records.

It allows users to add, view, update, and delete student details using API requests.

## Technologies Used
- Python
- Flask
- SQLite
- Pydantic
- Postman

## Features
- Add student details
- View all students
- View a single student
- Update student details
- Delete student details
- API Key Authentication
- Input validation
- Error handling

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /students | Add a student |
| GET | /students | View all students |
| GET | /students/1 | View one student |
| PUT | /students/1 | Update student |
| DELETE | /students/1 | Delete student |

## API Authentication
All student endpoints require an API key.

Header:
- Key: x-api-key
- Value: student123

## How to Run the Project

1. Clone the repository.
2. Install dependencies:

   pip install -r requirements.txt

3. Run the application:

   python app.py

4. Open:

   http://127.0.0.1:5000

## Testing
The API endpoints are tested using Postman.

## Learning Outcomes
- Understanding REST API development
- Creating CRUD operations
- Working with SQLite databases
- Validating user inputs
- Implementing API Key Authentication
- Testing APIs using Postman

## Author
Student Project
