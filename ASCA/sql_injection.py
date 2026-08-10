import sqlite3
import logging
import psycopg2
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# Database connection variable
db_connection = None

# Vulnerable function - SQL Injection vulnerability
@app.route('/vulnerable/user')
def get_user_by_id():
    """Vulnerable endpoint that demonstrates SQL injection"""
    # Get user ID from request parameter
    user_id = request.args.get('id', '')

    # VULNERABLE: Direct concatenation of user input into SQL query
    query = f"SELECT id, username, email FROM users WHERE id = {user_id}"

    print(f"Executing query: {query}")

    try:
        # Execute the vulnerable query
        cursor = db_connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        # Process results
        result = []
        for row in rows:
            result.append(f"User: ID={row[0]}, Username={row[1]}, Email={row[2]}")

        return Response('\n'.join(result), mimetype='text/plain')
    except Exception as e:
        logging.error(f"Query error: {e}")
        return Response("Database error", status=500)



def init_db():
    """Initialize database connection"""
    global db_connection
    try:
        # This is just for demonstration purposes - we're not actually connecting to a database
        # For PostgreSQL, you would use:
        # db_connection = psycopg2.connect(
        #     host="localhost",
        #     database="postgres",
        #     user="postgres",
        #     password="postgres"
        # )

        # Using SQLite for demonstration
        db_connection = sqlite3.connect(':memory:', check_same_thread=False)

        # Create a sample users table for demonstration
        cursor = db_connection.cursor()
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                email TEXT
            )
        ''')

        # Insert some sample data
        cursor.execute("INSERT INTO users (username, email) VALUES ('admin', 'admin@example.com')")
        cursor.execute("INSERT INTO users (username, email) VALUES ('user1', 'user1@example.com')")
        cursor.execute("INSERT INTO users (username, email) VALUES ('test', 'test@example.com')")
        db_connection.commit()

        print("Database connection example (using SQLite for demo)")
    except Exception as e:
        logging.error(f"DB connection error: {e}")
        return

# Secure function - Fixed version that prevents SQL Injection
@app.route('/secure/user')
def get_user_by_id_secure():
    """Secure endpoint that prevents SQL injection using parameterized queries"""
    # Get user ID from request parameter
    user_id = request.args.get('id', '')

    # SECURE: Using parameterized query with placeholders
    query = "SELECT id, username, email FROM users WHERE id = ?"

    try:
        # Execute the secure query with parameters
        cursor = db_connection.cursor()
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

        # Process results
        result = []
        for row in rows:
            result.append(f"User: ID={row[0]}, Username={row[1]}, Email={row[2]}")

        return Response('\n'.join(result), mimetype='text/plain')
    except Exception as e:
        logging.error(f"Query error: {e}")
        return Response("Database error", status=500)

# Another vulnerable function using string formatting
@app.route('/vulnerable/search')
def search_users():
    """Vulnerable search endpoint using string formatting"""
    # Get search query from request parameter
    search_term = request.args.get('q', '')

    # VULNERABLE: Using string formatting to construct SQL query
    query = f"SELECT id, username, email FROM users WHERE username LIKE '%{search_term}%'"

    print(f"Executing search query: {query}")

    try:
        # Execute the vulnerable query
        cursor = db_connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        # Process results
        result = []
        for row in rows:
            result.append(f"User: ID={row[0]}, Username={row[1]}, Email={row[2]}")

        return Response('\n'.join(result), mimetype='text/plain')
    except Exception as e:
        logging.error(f"Query error: {e}")
        return Response("Database error", status=500)

# Secure version of search_users
@app.route('/secure/search')
def search_users_secure():
    """Secure search endpoint using parameterized queries"""
    # Get search query from request parameter
    search_term = request.args.get('q', '')

    # SECURE: Using parameterized query with placeholders
    query = "SELECT id, username, email FROM users WHERE username LIKE ?"

    try:
        # Execute the secure query with parameters
        cursor = db_connection.cursor()
        cursor.execute(query, (f"%{search_term}%",))
        rows = cursor.fetchall()

        # Process results
        result = []
        for row in rows:
            result.append(f"User: ID={row[0]}, Username={row[1]}, Email={row[2]}")

        return Response('\n'.join(result), mimetype='text/plain')
    except Exception as e:
        logging.error(f"Query error: {e}")
        return Response("Database error", status=500)

def run_sql_examples():
    """Main function to run the SQL injection examples"""
    init_db()

    print("Server starting on port 8080...")
    print("Try SQL injection at: http://localhost:8080/vulnerable/user?id=1 OR 1=1")
    print("Try secure version at: http://localhost:8080/secure/user?id=1")
    print("Try SQL injection with string formatting at: http://localhost:8080/vulnerable/search?q=admin'--")
    print("Try secure search version at: http://localhost:8080/secure/search?q=admin")

    # Start server
    print("Server would start here if this was the main function")
    # app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    run_sql_examples()

"""
SQL Injection Attack Examples:

1. Return all users:
   http://localhost:8080/vulnerable/user?id=1 OR 1=1

2. Cause syntax error:
   http://localhost:8080/vulnerable/user?id=1'; DROP TABLE users; --

3. Union attack:
   http://localhost:8080/vulnerable/user?id=1 UNION SELECT username,password,email FROM users

4. Using string formatting vulnerability:
   http://localhost:8080/vulnerable/search?q=admin'--

5. SQL injection in LIKE clause:
   http://localhost:8080/vulnerable/search?q=a%' UNION SELECT id,password,email FROM users WHERE '1'='1

The secure version prevents these attacks by using parameterized queries
where user input is treated as data, not executable SQL code.

Dependencies needed:
pip install flask psycopg2-binary

Note: This example uses SQLite for demonstration purposes. In production,
you would typically use PostgreSQL, MySQL, or another database system.
For PostgreSQL, uncomment the psycopg2 connection code in init_db().
"""
