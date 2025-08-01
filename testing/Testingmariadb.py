import mariadb
import sys

# Database connection details
db_config = {
    'user': 'root',  # Replace with your MariaDB username
    'password': 'mariadb',  # Replace with your MariaDB password
    'host': 'localhost',  # Replace with your MariaDB host
    'database': 'mxtrading'  # Replace with your database name
}

conn = None
cursor = None

try:
    # Establish the connection
    conn = mariadb.connect(**db_config)
    
    # Create a cursor object
    cursor = conn.cursor()

    # --- Data Insertion Example ---
    # Create a table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50)
        )
    """)
    conn.commit()

    # Insert data
    first_name = "John"
    last_name = "Doe"
    insert_query = "INSERT INTO users (first_name, last_name) VALUES (?, ?)"
    for x in range(1, 1000000):  # Insert 999,999 records
        try:
            cursor.execute(insert_query, (first_name, last_name))
            conn.commit()
            # print(f"Successfully inserted user: {first_name} {last_name}")
            # print(f"Last Inserted ID: {cursor.lastrowid}")
        except mariadb.Error as e:
            # print(f"Error inserting data: {e}")
            conn.rollback() # Rollback in case of error

    # --- Data Retrieval Example ---
    # Select data
    # select_query = "SELECT id, first_name, last_name FROM users WHERE first_name = ?"
    # search_name = "John"
    # cursor.execute(select_query, (search_name,))

    # print(f"\nUsers with first name '{search_name}':")
    # for (user_id, retrieved_first_name, retrieved_last_name) in cursor:
    #     print(f"ID: {user_id}, Name: {retrieved_first_name} {retrieved_last_name}")

except mariadb.Error as e:
    print(f"Error connecting to or interacting with MariaDB: {e}")
    sys.exit(1)

finally:
    # Close cursor and connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("\nConnection closed.")