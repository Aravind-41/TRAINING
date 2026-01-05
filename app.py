from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import model


app = Flask(__name__, template_folder='static/templates', static_folder='static')
app.secret_key = 'dev-secret-change-me'

# Ensure the database and sample users exist at startup
model.ensure_db()


@app.route('/')
def index():
    username = session.get('username')
    return render_template('index.html', username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Support JSON (AJAX) and form submissions
        if request.is_json:
            data = request.get_json()
            username = (data.get('username') or '').strip()
            password = data.get('password') or ''
            ok = model.verify_user(username, password)
            if ok:
                session['username'] = username
                return jsonify(success=True, message='Logged in')
            return jsonify(success=False, message='Invalid credentials'), 401

        # regular form POST
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username and model.verify_user(username, password):
            session['username'] = username
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
            return render_template('login.html', username=username)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
