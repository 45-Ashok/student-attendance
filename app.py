from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "attendance.db"


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                UNIQUE(student_id, date)
            )
        """)


@app.route("/")
def home():
    with sqlite3.connect(DATABASE) as conn:
        students = conn.execute(
            "SELECT id, name FROM students ORDER BY id"
        ).fetchall()

    return render_template("index.html", students=students)


@app.route("/add_student", methods=["POST"])
def add_student():
    name = request.form.get("name", "").strip()

    if not name:
        return "Student name is required", 400

    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "INSERT INTO students (name) VALUES (?)",
            (name,)
        )

    return redirect("/")


@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    if request.method == "POST":
        student_id = request.form.get("student_id", type=int)
        date = request.form.get("date", "")
        status = request.form.get("status", "")

        if not student_id or not date or status not in (
            "Present", "Absent"
        ):
            return "Invalid attendance details", 400

        with sqlite3.connect(DATABASE) as conn:
            student = conn.execute(
                "SELECT id FROM students WHERE id = ?",
                (student_id,)
            ).fetchone()

            if student is None:
                return "Student not found", 404

            conn.execute("""
                INSERT INTO attendance
                    (student_id, date, status)
                VALUES (?, ?, ?)
                ON CONFLICT(student_id, date)
                DO UPDATE SET status = excluded.status
            """, (student_id, date, status))

        return redirect("/attendance")

    with sqlite3.connect(DATABASE) as conn:
        records = conn.execute("""
            SELECT students.name, attendance.date, attendance.status
            FROM attendance
            JOIN students
              ON students.id = attendance.student_id
            ORDER BY attendance.date DESC
        """).fetchall()

    return render_template(
        "attendance.html",
        records=records
    )


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)