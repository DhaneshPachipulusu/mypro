import mysql.connector

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "280902",  # Replace with your MySQL password
    "database": "my_database1"  # Replace with your database name
}

try:
    # Establishing a connection
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        print("Connection to the database was successful!")
    else:
        print("Connection failed.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if conn.is_connected():
        conn.close()
        print("Database connection closed.")
