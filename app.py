from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database connection
def get_db():
    return sqlite3.connect("tasks.db")

# Create table if not exists
conn = get_db()
conn.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, status TEXT)")
conn.close()

# Home page
@app.route('/')
def index():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Add task
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    conn = get_db()
    conn.execute("INSERT INTO tasks (title, status) VALUES (?, ?)", (title, 'Pending'))
    conn.commit()
    conn.close()
    return redirect('/')

# Mark complete
@app.route('/complete/<int:id>')
def complete(id):
    conn = get_db()
    conn.execute("UPDATE tasks SET status='Done' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Delete task
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

app.run(debug=True)