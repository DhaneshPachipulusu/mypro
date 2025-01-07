from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for sessions

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "280902",  # Replace with your MySQL password
    "database": "my_database1"   # Replace with your database name
}

# Render the login page (home)
@app.route('/')
def home():
    return render_template('login.html')

# Handle the login process
@app.route('/login', methods=['POST'])
# Handle the login process
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username_or_email = data['username']
        password = data['password']

        # Connect to MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if the username/email exists
        cursor.execute("SELECT username, email, password, role FROM users WHERE username = %s OR email = %s",
                       (username_or_email, username_or_email))
        user = cursor.fetchone()

        if user and user[2] == password:  # No hashing, directly compare password
            session['user_id'] = user[0]  # Store user ID in session
            session['role'] = user[3]     # Store user role in session

            # Redirect based on role
            if user[3] == 'user':
                return jsonify({"redirect": "/user_dashboard"}), 200
            elif user[3] == 'admin':
                return jsonify({"redirect": "/admin_dashboard"}), 200
            elif user[3] == 'superadmin':
                return jsonify({"redirect": "/superadmin_dashboard"}), 200

        else:
            return jsonify({"error": "Invalid username/email or password"}), 400
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Success page route
@app.route('/success')
def success_page():
    return render_template('1.html')

# Dashboard routes for different roles
# Route for user dashboard
@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

# Route for admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

# Route for superadmin dashboard
@app.route('/superadmin_dashboard')
def superadmin_dashboard():
    return render_template('superadmin_dashboard.html')

# Render the registration page for admin
@app.route('/register/admin')
def register_admin_page():
    return render_template('register_admin.html')

# Handle registration for admin (create a new admin user)
@app.route('/register/admin', methods=['POST'])
def register_admin():
    try:
        data = request.json
        username = data['username']
        email = data['work_email']
        password = data['password']  # Store password as plain text

        # Connect to MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if the username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            field = 'username' if existing_user[1] == username else 'email'
            return jsonify({"error": f"{field.capitalize()} already exists!", "field": field}), 400

        # Insert new admin user into the database with plain text password
        sql = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (username, email, password, 'admin'))
        conn.commit()

        return jsonify({"message": "Admin registration successful!"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Render the registration page for super admin
@app.route('/register/superadmin')
def register_superadmin_page():
    return render_template('register_superadmin.html')

# Handle registration for super admin
@app.route('/register/superadmin', methods=['POST'])
def register_superadmin():
    try:
        data = request.json
        username = data['username']
        email = data['work_email']
        password = data['password']  # Store password as plain text

        # Connect to MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if a super admin already exists
        cursor.execute("SELECT * FROM users WHERE role = 'superadmin'")
        existing_superadmin = cursor.fetchone()

        if existing_superadmin:
            return jsonify({"error": "Super Admin already exists!"}), 400

        # Check if the username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            field = 'username' if existing_user[1] == username else 'email'
            return jsonify({"error": f"{field.capitalize()} already exists!", "field": field}), 400

        # Insert new super admin user into the database with plain text password
        sql = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (username, email, password, 'superadmin'))
        conn.commit()

        return jsonify({"message": "Super Admin registration successful!"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Render the registration page for user
@app.route('/register/user')
def register_user_page():
    return render_template('register_user.html')  # Ensure you have a separate HTML file for user registration

# Handle registration for user (create a new user account)
@app.route('/register/user', methods=['POST'])
def register_user():
    try:
        data = request.json
        username = data['username']
        email = data['email']
        password = data['password']  # Store password as plain text

        # Connect to MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if the username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            field = 'username' if existing_user[1] == username else 'email'
            return jsonify({"error": f"{field.capitalize()} already exists!", "field": field}), 400

        # Insert new user into the database with plain text password
        sql = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (username, email, password, 'user'))
        conn.commit()

        return jsonify({"message": "User registration successful!"}), 201


    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

