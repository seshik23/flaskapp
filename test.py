import sqlite3

# Connect to the SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('mydatabase.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    filename TEXT,
    word_count INTEGER
);
''')

# Insert data into the users table
users_data = [
    ('john_doe', 'password123', 'John', 'Doe', 'john.doe@example.com', 'file1.txt', 500),
    ('jane_smith', 'securepass456', 'Jane', 'Smith', 'jane.smith@example.com', 'file2.txt', 750),
    ('alice_wonder', 'mypassword789', 'Alice', 'Wonder', 'alice.wonder@example.com', 'file3.txt', 600),
    ('bob_builder', 'buildit987', 'Bob', 'Builder', 'bob.builder@example.com', 'file4.txt', 800)
]

cursor.executemany('''
INSERT INTO users (username, password, firstname, lastname, email, filename, word_count) 
VALUES (?, ?, ?, ?, ?, ?, ?);
''', users_data)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully.")

