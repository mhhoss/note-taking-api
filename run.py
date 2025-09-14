from flask import Flask, redirect, render_template, request
import sqlite3
from config import DATABASE


app = Flask(__name__)


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # برای دسترسی به نام ستون
    return conn


@app.route('/')
def index():
    conn = get_db() # تابعی برای گرفتن دیتابیس
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes')
    notes = cursor.fetchall()
    conn.close()
    return render_template('index.html', notes=notes)


@app.route('/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        return render_template('create_note.html')


@app.route('/update/<int:id>', methods=['GET'])
def update_note(id):
    """
    ویرایش یادداشت با شناسه آیدی:
    GET: نمایش فرم و داده فعلی
    POST: ذخیره تغییرات
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE id = ?', (id,))
    note = cursor.fetchone()
    conn.close()

    if not note:
        conn.close()
        return 'هنوز یادداشتی وجود ندارد'
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute('UPDATE notes SET title = ?, content = ? WHERE id = ?', (title, content, id))
        conn.commit()
        conn.close()
        return redirect('/')

    conn.close()
    return render_template('update_note.html', note=note)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_note(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
