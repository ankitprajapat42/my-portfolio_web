from flask import Flask, render_template, request, redirect, session, url_for
import os
import json
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)
app.secret_key = 'supersecretankit123!'

# Secure Firebase Admin SDK initialization
if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON"):
    cred_dict = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
    cred = credentials.Certificate(cred_dict)
else:
    cred = credentials.Certificate("service_account_key.json")  # fallback for local testing

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://myportfolio-8c965-default-rtdb.firebaseio.com'
})

# ----------- All your existing routes remain same (no change) ------------ #

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "ankit@admin" and password == "ankit@9413":
            session['admin'] = True
            return redirect('/dashboard')
        else:
            return render_template('admin_login.html', error="Invalid credentials")
    return render_template('admin_login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/admin')
    data = db.reference('data').get()
    return render_template('admin_dashboard.html', data=data)

# All edit routes (unchanged)
# edit-profile, edit-skills, edit-languages, edit-projects, edit-experience, etc.
# Keep them as you wrote above.

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/admin')

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/pge')
def home():
    ref = db.reference('data')
    user_data = ref.get()
    return render_template("home.html", data=user_data)

@app.route('/')
def index():
    ref = db.reference('data')
    user_data = ref.get()
    return render_template("index.html", data=user_data)

# # ✅ App Run (keep this at bottom only)
# if __name__ == '__main__':
#     app.run(debug=True, port=1000, host='0.0.0.0')
