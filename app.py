from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
app.secret_key = "mentora_secret"

# Email setup
SENDER_EMAIL = "anilkumar22.analyst@gmail.com"
APP_PASSWORD = "wwfi hdbz zwvi vpbi"  # Gmail App Password


def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        course = request.form["course"]

        admin_subject = f"New Admission Form: {name}"
        admin_body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nCourse: {course}"
        user_subject = "Thank You for Registering with Mentora Institute"
        user_body = f"Dear {name},\n\nThank you for registering! We'll contact you soon.\n\nBest regards,\nMentora Institute"

        send_email("anilkumar22.analyst@gmail.com", admin_subject, admin_body)
        send_email(email, user_subject, user_body)

        flash("✅ Thank you for registering! We’ll contact you soon.", "success")
        return redirect(url_for("join"))
    return render_template("join.html")


@app.route("/enquiry", methods=["GET", "POST"])
def enquiry():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        query = request.form["query"]

        admin_subject = f"New Enquiry from {name}"
        admin_body = f"Name: {name}\nEmail: {email}\nQuery: {query}"
        user_subject = "Thank You for Contacting Mentora Institute"
        user_body = f"Dear {name},\n\nWe’ve received your enquiry and will get back soon.\n\nBest regards,\nMentora Institute"

        send_email("anilkumar22.analyst@gmail.com", admin_subject, admin_body)
        send_email(email, user_subject, user_body)

        flash("📩 Enquiry submitted successfully!", "success")
        return redirect(url_for("enquiry"))
    return render_template("enquiry.html")


if __name__ == "__main__":
    app.run(debug=True)
