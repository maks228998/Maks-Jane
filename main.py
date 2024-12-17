import psycopg2, os
from flask import Flask, request, jsonify, render_template, redirect, session, url_for, flash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = 'maks_jane_lr'

limiter = Limiter(
    get_remote_address,
    app = app,
    default_limits = ["200 per day", "5 per hour"],
    storage_uri = "memory://",
)

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="db",
            database="tasks",
            user="postgres",
            password="1"
        )
        return conn
    except psycopg2.Error as e:
        print(f"error: {e}")
        return None

def check_db_exists():
    try:
        conn = get_db_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS logins ("
                       "logins_id SERIAL PRIMARY KEY,"
                       "logins_login VARCHAR(50) NOT NULL UNIQUE,"
                       "logins_password VARCHAR(255) NOT NULL);")

        cursor.execute("CREATE TABLE IF NOT EXISTS profile ("
                       "profile_id SERIAL PRIMARY KEY, "
                       "profile_login VARCHAR(50) NOT NULL UNIQUE, "
                       "profile_first_name VARCHAR(100) NOT NULL,"
                       "profile_name VARCHAR(100) NOT NULL, "
                       "profile_second_name VARCHAR(100) NOT NULL, "
                       "profile_phone VARCHAR(20) NOT NULL  UNIQUE, "
                       "profile_email VARCHAR(100) NOT NULL UNIQUE);")

        cursor.execute("CREATE TABLE IF NOT EXISTS comments ("
                       "comments_id SERIAL PRIMARY KEY, "
                       "comments_date DATE NOT NULL, "
                       "comments_time VARCHAR(10) NOT NULL, "
                       "comments_profile_id INTEGER NOT NULL, "
                       "comments_text VARCHAR(1000) NOT NULL, "
                       "FOREIGN KEY (comments_profile_id) REFERENCES profile(profile_id));")

        cursor.execute("CREATE TABLE IF NOT EXISTS feedback ("
                       "feedback_id SERIAL PRIMARY KEY, " 
                       "feedback_date DATE NOT NULL, "
                       "feedback_time VARCHAR(100) NOT NULL, "
                       "feedback_name VARCHAR(100) NOT NULL, "
                       "feedback_email VARCHAR(100) NOT NULL, "
                       "feedback_text VARCHAR(1000) NOT NULL);")

        cursor.execute("INSERT INTO profile (profile_id, profile_login, profile_first_name, profile_name, profile_second_name, profile_phone, profile_email)"
                       "VALUES ('1', 'DELETED', 'DELETED', 'DELETED', 'DELETED', '123-456-7890', 'remote_user@example.com') "
                       "ON CONFLICT (profile_login) DO NOTHING;")

        cursor.execute("INSERT INTO logins (logins_id. logins_login, logins_password) VALUES ('1', 'DELETED', ' ') "
                       "ON CONFLICT (logins_login) DO NOTHING;")

        conn.commit()
        conn.close()
        return 0
    except Exception as e:
        print(f"error: {e}")
        return []

def add_feedback(name, email, message):
    try:
        conn = get_db_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (feedback_date, feedback_time, feedback_name, feedback_email, feedback_text) "
                       "VALUES (CURRENT_DATE, TO_CHAR(NOW(), 'HH24:MI'), %s, %s, %s)",
                       (name, email, message))

        conn.commit()
        conn.close()
        return 0
    except Exception as e:
        print(f"error: {e}")
        return []

def check_user_exists(login):
    try:
        conn = get_db_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logins "
                       "WHERE logins_login =%s)",
                       (login,))
        user = cursor.fetchall()

        conn.commit()
        conn.close()
        return user
    except Exception as e:
        print(f"error: {e}")
        return []

def add_user(login, password, first_name, name, second_name, phone, email):
    try:
        conn = get_db_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        cursor.execute("INSERT INTO logins (logins_login, logins_password) "
                       "VALUES (%s, %s)",
                       (login, password))
        cursor.execute("INSERT INTO profile (profile_login, profile_first_name, profile_name, profile_second_name, profile_phone, profile_email) "
                       "VALUES (%s, %s, %s, %s, %s, %s)",
                     (login, first_name, name, second_name, phone, email))

        conn.commit()
        conn.close()
        return 0
    except Exception as e:
        print(f"error: {e}")
        return []

def get_profile(login):
    try:
        conn = get_db_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT profile_login, profile_first_name, profile_name, profile_second_name, profile_phone, profile_email "
                       "FROM profile where profile_login = %s",
                       (str(login),))
        profile = cursor.fetchone()
        conn.commit()
        conn.close()
        return profile
    except Exception as e:
        print(f"error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return []

def add_comment(login, comment):
    try:
        conn = get_db_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT profile_id FROM profile  "
                       "WHERE (profile_login = %s)",
                       (login,))
        profile_id = cursor.fetchall()
        cursor.execute("INSERT INTO comments (comments_date, comments_time, comments_profile_id, comments_text) "
                     "VALUES (CURRENT_DATE, TO_CHAR(NOW(), 'HH24:MI'), %s, %s)",
                     (profile_id[0], comment))

        conn.commit()
        conn.close()
        return 0
    except Exception as e:
        print(f"error: {e}")
        return []

def get_comments():
    try:
        conn = get_db_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT profile.profile_login, comments.comments_date, comments.comments_time, comments.comments_text "
                     "FROM comments "
                     "JOIN profile ON comments.comments_profile_id = profile.profile_id;")
        comments = cursor.fetchall()

        conn.commit()
        conn.close()
        return comments
    except Exception as e:
        print(f"error: {e}")
        return []

def del_user(login,password):
    try:
        conn = get_db_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT profile_id FROM profile  "
                       "WHERE (profile_login = %s)",
                       (login,))
        profile_id = cursor.fetchone()
        cursor.execute("UPDATE comments "
                       "SET comments_profile_id = '1' "
                       "WHERE (comments_profile_id = %s)",
                       (profile_id[0],))
        cursor.execute("DELETE FROM logins "
                       "WHERE (logins_login = %s and logins_password = %s)",
                       (login,password))
        cursor.execute("DELETE FROM profile "
                       "WHERE (profile_login = %s)",
                       (login,))

        conn.commit()
        conn.close()
        return 0
    except Exception as e:
        print(f"error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return 1

def get_login(login, password):
    try:
        conn = get_db_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logins "
                       "WHERE logins_login = %s AND logins_password = %s",
                       (login, password))
        db_login = cursor.fetchone()
        conn.commit()
        conn.close()
        return db_login
    except Exception as e:
        print(f"error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return []

def update_user(new_login, login, first_name, name, second_name, phone, email):
    try:
        conn = get_db_connection()
        if conn is None:
            return []

        cursor = conn.cursor()
        cursor.execute("UPDATE profile "
                       "SET profile_login = %s, profile_first_name = %s, profile_name = %s, profile_second_name = %s, profile_phone = %s, profile_email = %s "
                       "WHERE profile_login = %s;",
                       (str(new_login), str(first_name), str(name), str(second_name), str(phone), str(email), str(login)))
        cursor.execute("UPDATE logins "
                       "SET logins_login = %s"
                       "WHERE logins_login = %s",
                       (str(new_login), str(login)))

        conn.commit()
        conn.close()
        return 0
    except Exception as e:
        print(f"error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return []

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

        login = data.get('login')
        password = data.get('password')

        if not login or not password:
            return jsonify({'error': 'Username or password is missing'}), 400

        if len(get_login(login, password)) == 0:
            return jsonify({'error': 'Username or password is incorrect'}), 400

        session['login'] = login
        session['password'] = password

        return jsonify({'redirect': url_for('profile')})

    if request.method == 'GET':
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        name = request.form.get('name')
        second_name = request.form.get('second_name')
        phone = request.form.get('phone')
        email = request.form.get('email')

        if (not login or
                not password or
                not first_name or
                not name or
                not second_name or
                not phone or
                not email):
            return jsonify({'error': 'Not all data received'}), 400

        if len(check_user_exists(login)) == 0:
            add_user(login, password, first_name, name, second_name, phone, email)

            session['login'] = login
            session['password'] = password
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('register'))

        return redirect(url_for('register'))

    if request.method == 'GET':
        return render_template('register.html')

@app.route('/profile', methods=['GET'])
def profile():
    session_login = session.get('login')

    if session_login is None:
        return redirect(url_for('login'))

    row = get_profile(session_login)

    profile_data = {
        'profile_login': row[0],
        'profile_first_name': row[1],
        'profile_name': row[2],
        'profile_second_name': row[3],
        'profile_phone': row[4],
        'profile_email': row[5]
    }

    return render_template('profile.html', profile=profile_data)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    session_login = session.get('login')

    if session_login is None:
        return redirect(url_for('login'))

    if request.method == 'GET':
        row = get_profile(session_login)
        profile_data = {
            'profile_login': row[0],
            'profile_first_name': row[1],
            'profile_name': row[2],
            'profile_second_name': row[3],
            'profile_phone': row[4],
            'profile_email': row[5]
        }

        return render_template('edit_profile.html', profile=profile_data)

    if request.method == 'POST':
        session_password = session.get('password')

        login = request.form.get('login')
        first_name = request.form.get('first_name')
        name = request.form.get('name')
        second_name = request.form.get('second_name')
        phone = request.form.get('phone')
        email = request.form.get('email')

        if (not login or
                not first_name or
                not name or
                not second_name or
                not phone or
                not email):
            return jsonify({'error': 'Not all data received'}), 400

        update_user(login, session_login, first_name, name, second_name, phone, email)

        session.clear()
        session['login'] = login
        return redirect(url_for('profile'))

@app.route('/delete_profile', methods=['GET', 'POST'])
def delete_profile():
    session_login = session.get('login')

    if session_login is None:
        return redirect(url_for('login'))

    if request.method == 'POST':
        password = request.form['password']
        password2 = request.form['password2']

        if not password or not password2:
            return redirect(url_for('delete_profile'))

        session_password = session.get('password')

        if password != password2 or session_password != password:
            return redirect(url_for('delete_profile'))

        if del_user(session_login , session_password) > 0:
            return redirect(url_for('delete_profile'))

        session.clear()
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('delete_profile.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    session_login = session.get('login')

    if session_login is None:
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_comment = request.form['new-comment']
        add_comment(session_login,  new_comment)

        return redirect(url_for('comments'))

    if request.method == 'GET':
        comments = get_comments()
        comments_list = []
        for comment in comments:
            comments_list.append({
                'username': comment[0],
                'comments_date': comment[1].strftime('%Y-%m-%d'),
                'comments_time': comment[2],
                'comments_text': comment[3],
            })

        return render_template('comments.html', comments=comments_list)

@app.route('/feedback', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        add_feedback(name, email, message)
        flash('Ваш отзыв успешно отправлен!', 'success')
        return redirect(url_for('feedback'))

    if request.method == 'GET':
        return render_template('feedback.html')

if __name__ == '__main__':
    e = check_db_exists()
    if e:
        print(f"error: {e}")
        os._exit(-1)
    app.run(debug=True, host='0.0.0.0')