from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector

app = Flask(__name__, static_folder="static")
CORS(app)

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Saleem@786",
    database = "student_management"
)

print("Database Connected Successfully")

cursor = conn.cursor(dictionary=True)
@app.route("/", methods=["GET"] )
def home_page():
    return app.send_static_file("index.html")

@app.route("/api/students", methods=["GET"])
def get_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return jsonify(students)


@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.json

    full_name = data.get("full_name")
    email = data.get("email")
    phone = data.get("phone")
    course = data.get("course")

    # VALIDATION
    if not all([full_name, email, phone, course]):
        return jsonify({"error": "All fields are required"}), 400

    try:
        query = """
            INSERT INTO students (full_name, email, phone, course)
            VALUES (%s, %s, %s, %s)
        """

        values = (full_name, email, phone, course)

        cursor.execute(query, values)
        conn.commit()

        return jsonify({
            "message": "Student added successfully"
        }), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    

@app.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.json

    full_name = data.get("full_name")
    email = data.get("email")
    phone = data.get("phone")
    course = data.get("course")

    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cursor.fetchone()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    query = """
        UPDATE students
        SET full_name=%s, email=%s, phone=%s, course=%s
        WHERE id=%s
    """

    values = (full_name, email, phone, course, id)

    cursor.execute(query, values)
    conn.commit()

    return jsonify({"message": "Student updated successfully"})

@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cursor.fetchone()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    cursor.execute("DELETE FROM students WHERE id = %s", (id,))
    conn.commit()

    return jsonify({"message": "Student deleted successfully"})


@app.route("/api/students/search", methods=["GET"])
def search_students():

    q = request.args.get("q", "")

    query = """
        SELECT * FROM students
        WHERE full_name LIKE %s
        OR course LIKE %s
    """

    search_term = f"%{q}%"

    cursor.execute(query, (search_term, search_term))

    students = cursor.fetchall()

    return jsonify(students)


if __name__ == "__main__":
    app.run(debug=True)

