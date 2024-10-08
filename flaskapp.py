from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

UPLOAD_FOLDER = '/home/ubuntu/flaskapp/uploads/'
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# SQLite setup
conn = sqlite3.connect('/home/ubuntu/flaskapp/mydatabase.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (username TEXT, password TEXT, firstname TEXT, lastname TEXT, email TEXT)''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        word_count = 0

        # Check if the username already exists
        conn = sqlite3.connect('/home/ubuntu/flaskapp/mydatabase.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = c.fetchone()

        if existing_user:
            flash("Oops! That username is already in use. Try another one.")
            return redirect(url_for('register'))

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as f:
                content = f.read()
                word_count = len(content.split())

        conn = sqlite3.connect('/home/ubuntu/flaskapp/mydatabase.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, firstname, lastname, email, filename, word_count) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (username, password, firstname, lastname, email, filename, word_count))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile/<username>')
def profile(username):
    # Check if the user is logged in
    if 'username' not in session:
        flash("Please log in to continue.")
        return redirect(url_for('login'))
    conn = sqlite3.connect('/home/ubuntu/flaskapp/mydatabase.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    return render_template('profile.html', user=user)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('/home/ubuntu/flaskapp/mydatabase.db', check_same_thread=False)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['username'] = user
            return redirect(url_for('profile', username=user[1]))
        else:
            flash("Login failed. Please check your credentials and try again.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove the username from the session if it's there
    session.pop('username', None)
    flash("Logout complete. See you next time!")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
