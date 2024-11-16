from flask import Flask, request, jsonify, render_template, redirect, session, flash, url_for
import json, psycopg2, os, bcrypt

app = Flask(__name__)
app.secret_key = 'maks_jane_lr'

def check_db_exists():
    try:
        conn = psycopg2.connect(
        host = "localhost",
        database = "tasks",
        user = "postgres",
        password = "1")

        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS logins ("
                       "logins_id SERIAL PRIMARY KEY,"
                       "logins_login VARCHAR(50) NOT NULL UNIQUE,"
                       "logins_password VARCHAR(255) NOT NULL);")
        cursor.execute("CREATE TABLE IF NOT EXISTS profile ("
                       "profile_id SERIAL PRIMARY KEY, "
                       "profile_login VARCHAR(50) NOT NULL UNIQUE, "
                       "profile_first_name VARCHAR(100) NOT NULL,"
                       "users_name VARCHAR(100) NOT NULL, "
                       "users_second_name VARCHAR(100) NOT NULL, "
                       "profile_phone VARCHAR(20) NOT NULL  UNIQUE, "
                       "profile_email VARCHAR(100) NOT NULL UNIQUE);")

        conn.commit()
        conn.close()
        return 0
    except psycopg2.Error as e:
        print(f"error: {e}")
        return e

def get_db_data(querry):
    try:
        conn = psycopg2.connect(
        host = "localhost",
        database = "tasks",
        user = "postgres",
        password = "1")

        print(querry)

        cursor = conn.cursor()
        cursor.execute(querry)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        print(rows)
        return rows
    except psycopg2.Error as e:
        print(f"error: {e}")
        return e

def put_db_data(querry):
    try:
        conn = psycopg2.connect(
        host = "localhost",
        database = "tasks",
        user = "postgres",
        password = "1")

        print(querry)

        cursor = conn.cursor()
        cursor.execute(querry)
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        print(affected_rows)
        return affected_rows
    except psycopg2.Error as e:
        print(f"error: {e}")
        return e

def del_db_data(querry):
    try:
        conn = psycopg2.connect(
        host = "localhost",
        database = "tasks",
        user = "postgres",
        password = "1")

        print(querry)

        cursor = conn.cursor()
        cursor.execute(querry)
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        print(affected_rows)
        return affected_rows
    except psycopg2.Error as e:
        print(f"error: {e}")
        return e

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

        db_data = get_db_data("SELECT * FROM logins where "
                              "logins_login ='" + login +
                              "' and logins_password = '" + password + "'" )

        if len(db_data) == 0:
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

        db_data = get_db_data("SELECT * FROM logins where "
                              "logins_login ='" + login + "'")

        if len(db_data) == 0:
            put_db_data("INSERT INTO logins ("
                        "logins_login, "
                        "logins_password"
                        ") VALUES ('" +
                        login + "', '" +
                        password + "')")
            put_db_data("INSERT INTO profile ("
                        "profile_login, "
                        "profile_first_name, "
                        "profile_name, "
                        "profile_second_name, "
                        "profile_phone, "
                        "profile_email"
                        ") VALUES ('" +
                        login + "', '" +
                        first_name + "', '" +
                        name + "', '" +
                        second_name + "', '" +
                        phone + "', '" +
                        email + "')")

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
    login = session.get('login')

    if login is None:
        return redirect(url_for('login'))

    db_data = get_db_data("SELECT "
                          "profile_login, "
                          "profile_first_name, "
                          "profile_name, "
                          "profile_second_name, "
                          "profile_phone, "
                          "profile_email "
                          "FROM profile where "
                          "profile_login = '" + login + "'")

    row = db_data[0]
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
    if request.method == 'GET':
        session_login = session.get('login')

        if session_login is None:
            return redirect(url_for('login'))

        db_data = get_db_data("SELECT "
                              "profile_login, "
                              "profile_first_name, "
                              "profile_name, "
                              "profile_second_name, "
                              "profile_phone, "
                              "profile_email "
                              "FROM profile where "
                              "profile_login = '" + session_login + "'")

        row = db_data[0]
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
        session_login = session.get('login')
        if session_login is None:
            return redirect(url_for('login'))

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

        db_data = get_db_data("SELECT * FROM logins where "
                              "logins_login ='" + session_login + "'")

        put_db_data("UPDATE profile SET "
                    "profile_login = '" + login + "', " +
                    "profile_first_name = '" + first_name + "', " +
                    "profile_name = '" + name + "', " +
                    "profile_second_name = '" + second_name + "', " +
                    "profile_phone = '" + phone + "', " +
                    "profile_email = '" + email + "' " +
                    "WHERE "
                    "profile_login = '" + session_login + "'")

        put_db_data("UPDATE logins SET "
                    "logins_login = '" + login +
                    "' WHERE "
                    "logins_login = '" + session_login + "'")

        session.clear()
        session['login'] = login
        return redirect(url_for('profile'))

@app.route('/delete_profile', methods=['GET', 'POST'])
def delete_profile():
    if request.method == 'POST':
        session_login = session.get('login')
        session_password = session.get('password')

        if session_login is None:
            return redirect(url_for('login'))

        data = request.get_json()

        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

        login = data.get('login')
        password = data.get('password')

        if not login or not password:
            return jsonify({'error': 'Username or password is missing'}), 400

        db_data = get_db_data(
            "SELECT * FROM logins where "
            "logins_login ='" + login +
            "' and logins_password = '" + password + "'")

        if len(db_data) == 0 or session_login != login or session_password != password:
            return jsonify({'error': 'Username or password is incorrect'}), 400

        del_db_data("DELETE FROM logins where "
                    "logins_login ='" + login +
                    "' and logins_password = '" + password + "'")
        del_db_data("DELETE FROM profile where "
                    "profile_login ='" + login + "'")

        session.clear()

        return jsonify({'redirect': url_for('login')})

    if request.method == 'GET':
        return render_template('delete_profile.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    e = check_db_exists()
    if e:
        print(f"error: {e}")
        os._exit(-1)
    app.run(debug=True)