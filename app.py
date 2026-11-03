
from flask import Flask, jsonify, request
from database import init_db, get_db_connection
from models import Student
from pydantic import ValidationError
from functools import wraps
import sqlite3

app = Flask(__name__)

# API Key Authentication
API_KEY = "student123"


def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = request.headers.get("x-api-key")

        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401

        return func(*args, **kwargs)

    return wrapper


# Home API
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Student Management API",
        "status": "Running successfully"
    })


# POST - Add Student
@app.route('/students', methods=['POST'])
@require_api_key
def add_student():
    try:
        body = request.get_json(silent=True)

        if body is None:
            return jsonify({"error": "Please provide JSON data"}), 400

        data = Student(**body)

        conn = get_db_connection()
        cursor = conn.execute(
            "INSERT INTO students (name, department, email) VALUES (?, ?, ?)",
            (data.name, data.department, data.email)
        )

        student_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return jsonify({
            "message": "Student added successfully!",
            "student_id": student_id
        }), 201

    except ValidationError as error:
        return jsonify({"errors": error.errors()}), 400

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409


# GET - View All Students
@app.route('/students', methods=['GET'])
@require_api_key
def get_students():
    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students]), 200


# GET - View One Student
@app.route('/students/<int:student_id>', methods=['GET'])
@require_api_key
def get_student(student_id):
    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()
    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student)), 200


# PUT - Update Student
@app.route('/students/<int:student_id>', methods=['PUT'])
@require_api_key
def update_student(student_id):
    try:
        body = request.get_json(silent=True)

        if body is None:
            return jsonify({"error": "Please provide JSON data"}), 400

        data = Student(**body)

        conn = get_db_connection()
        cursor = conn.execute(
            """UPDATE students
               SET name = ?, department = ?, email = ?
               WHERE id = ?""",
            (data.name, data.department, data.email, student_id)
        )

        conn.commit()
        updated = cursor.rowcount
        conn.close()

        if updated == 0:
            return jsonify({"error": "Student not found"}), 404

        return jsonify({
            "message": "Student updated successfully!"
        }), 200

    except ValidationError as error:
        return jsonify({"errors": error.errors()}), 400

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409


# DELETE - Delete Student
@app.route('/students/<int:student_id>', methods=['DELETE'])
@require_api_key
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({
        "message": "Student deleted successfully!"
    }), 200


if __name__ == '__main__':
    init_db()
    print("Database created successfully!")
    app.run(debug=True)
