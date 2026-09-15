from multiprocessing.dummy import connection
from sqlite3 import Cursor

from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv 
import os

from werkzeug.security import generate_password_hash, check_password_hash

from db import get_connection

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated_function

@app.route("/")
@login_required
def home():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
            SELECT id, company, role_title, status, applied_date
            FROM applications
            WHERE user_id = %s
            ORDER BY applied_date DESC
            LIMIT 3
            """,
            (session["user_id"],)
    )

    applications = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("dashboard.html", applications=applications)


@app.route("/applications")
@login_required
def applications():

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT * FROM applications
        WHERE user_id = %s
        ORDER BY applied_date DESC
        """,
        (session["user_id"],)
    )

    applications = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template(
        "applications.html",
        applications=applications,
        search_query=""
    )

@app.route("/applications/new", methods=["GET"])
@login_required
def new_application():
    return render_template("add_applications.html")

@app.route("/applications/new", methods=["POST"])
@login_required
def add_application():

    company = request.form.get("company", "").strip()
    role_title = request.form.get("role_title", "").strip()
    applied_date = request.form.get("applied_date", "").strip()

    if not company or not role_title or not applied_date:
        return "All fields are required.", 400

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO applications
            (
                user_id,
                company,
                role_title,
                applied_date
            )
            VALUES
            (%s, %s, %s, %s)
            """,
            (
                session["user_id"],
                company,
                role_title,
                applied_date
            )
        )

        connection.commit()

        return redirect("/applications")

    except Exception:
        if connection:
            connection.rollback()

        return "Unable to save the application. Please try again.", 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.route("/api/applications/<int:id>/status", methods=["PATCH"])
@login_required
def update_application_status(id):

    data = request.get_json()

    if not data:
        return {
            "error": "Request body is required"
        }, 400

    allowed_statuses = [
        "Applied",
        "Screening",
        "Interviewing",
        "Offer",
        "Rejected"
    ]

    new_status = data.get("status")

    if not new_status:
        return {
            "error": "Status is required"
        }, 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE applications
        SET status = %s
        WHERE id = %s
        AND user_id = %s
        """,
        (new_status, id, session["user_id"])
    )

    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        return {
            "error": "Application not found or access denied"
        }, 404

    connection.commit()
    cursor.close()
    connection.close()

    return{
        "message": "Application status updated successfully",
        "status": new_status
    }, 200

@app.route("/applications/<int:id>/delete", methods=["POST"])
@login_required
def delete_application(id):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM applications
            WHERE id = %s
            AND user_id = %s
            """,
            (
                id,
                session["user_id"]
            )
        )

        if cursor.rowcount == 0:
            connection.rollback()

            return "Application not found or access denied", 404

        connection.commit()

        return redirect("/applications")

    except Exception:
        if connection:
            connection.rollback()

        return "An error occurred while deleting the application.", 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.route("/api/metrics")
@login_required
def get_metrics():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total_applied
        FROM applications
        WHERE user_id = %s
    """, (session["user_id"],))

    total_applied = cursor.fetchone()["total_applied"]

    cursor.execute("""
        SELECT COUNT(*) AS total_interviews
        FROM applications
        WHERE status = 'Interviewing'
        AND user_id = %s
    """, (session["user_id"],))

    total_interviews = cursor.fetchone()["total_interviews"]

    cursor.execute("""
        SELECT COUNT(*) AS total_offers
        FROM applications
        WHERE status = 'Offer'
        AND user_id = %s
    """, (session["user_id"],))

    total_offers = cursor.fetchone()["total_offers"]

    if total_applied > 0:
        interview_rate = (total_interviews / total_applied) * 100
    else:
        interview_rate = 0

    cursor.close()
    connection.close()

    return {
        "total_applied": total_applied,
        "interview_rate": round(interview_rate, 2),
        "offers": total_offers
    }

@app.route("/applications/search")
@login_required
def search_applications():

    query = request.args.get("q", "").strip()
    if not query:
        return redirect("/applications")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
    """
    SELECT id, company, role_title, status, applied_date
    FROM applications
    WHERE user_id = %s
    AND (
        company LIKE %s
        OR role_title LIKE %s
    )
    ORDER BY applied_date DESC
    """,
    (
        session["user_id"],
        f"%{query}%",
        f"%{query}%"
    )
)

    applications = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "applications.html",
        applications = applications,
        search_query = query
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user: 
            cursor.close()
            connection.close()
            return render_template("register.html", error="An account with this email already exists.")

        password_hash = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users (email, password_hash)
            VALUES (%s, %s)
            """,
            (email, password_hash)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method =="POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, email, password_hash
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and check_password_hash(user["password_hash"], password):

            session["user_id"] = user["id"]
            session["email"] = user["email"]

            return redirect("/")
        return render_template("login.html", error="Invalid email or password.")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.errorhandler(404)
def page_not_found(error):
    return "Page not found.", 404

@app.errorhandler(500)
def internal_server_error(error):
    return "Something went wrong on the server.", 500

if __name__ =="__main__":
    app.run()
