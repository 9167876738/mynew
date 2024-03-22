from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'saket#123'

# Configure MySQL
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Rohini@1970',
    database='hostel_db'
)

# Create a cursor object
cursor = db.cursor()

def validate_email(email):
    # Simple email validation using regular expression
    pattern = r"^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$"
    return re.match(pattern, email)

def validate_phone(phone):
    # Simple phone number validation
    pattern = r"^[0-9]{10}$"
    return re.match(pattern, phone)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['uname']
        email = request.form['email']
        password = request.form['psw']

        # Validation
        if not (name and email and password):
            return "Please fill in all required fields."

        if not validate_email(email):
            return "Invalid email format."

        if len(password) < 8:
            return "Password must be at least 8 characters long."

        hashed_password = generate_password_hash(password)

        # Inserting data into the database
        sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        values = (name, email, hashed_password)
        cursor.execute(sql, values)
        db.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('psw')

        # Validation
        if not (email and password):
            return "Please fill in all required fields."

        if not validate_email(email):
            return "Invalid email format."

        # Fetch user from the database
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))

        return "Invalid email or password."

    return render_template('login.html')

@app.route('/', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        # Validation
        if not (name and email and phone and address):
            return "Please fill in all required fields."

        if not validate_email(email):
            return "Invalid email format."

        if not validate_phone(phone):
            return "Invalid phone number format."

        # Inserting data into the database
        sql = "INSERT INTO students (name, email, phone, address) VALUES (%s, %s, %s, %s)"
        values = (name, email, phone, address)
        cursor.execute(sql, values)
        db.commit()

        return redirect(url_for('dashboard'))

    return render_template('add_student.html')

@app.route('/delete_student/<int:student_id>', methods=['GET'])
def delete_student(student_id):
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    db.commit()
    return redirect(url_for('dashboard'))

@app.route('/update_student/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    if request.method == 'POST':
        updated_name = request.form['name']
        updated_email = request.form['email']
        updated_phone = request.form['phone']
        updated_address = request.form['address']

        # Validation
        if not (updated_name and updated_email and updated_phone and updated_address):
            return "Please fill in all required fields."

        if not validate_email(updated_email):
            return "Invalid email format."

        if not validate_phone(updated_phone):
            return "Invalid phone number format."

        # Update student information in the database
        update_query = "UPDATE students SET name = %s, email = %s, phone = %s, address = %s WHERE id = %s"
        update_values = (updated_name, updated_email, updated_phone, updated_address, student_id)
        cursor.execute(update_query, update_values)
        db.commit()

        return redirect(url_for('dashboard'))

    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    return render_template('update_student.html', student=student)

@app.route('/show_students', methods=['GET'])
def show_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('show_students.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)
