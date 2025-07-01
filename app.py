from flask import Flask, render_template, request, redirect, session, url_for
from firebase import firebase
import firebase_admin
from firebase_admin import credentials, db
app = Flask(__name__)
app.secret_key = 'supersecretankit123!'

config = {
  "apiKey": "AIzaSyCh_um2Zdrgycz_6aKf7_Qscn_mw2O7FkI",
  "authDomain": "myportfolio-8c965.firebaseapp.com",
  "databaseURL": "https://myportfolio-8c965-default-rtdb.firebaseio.com",
  "projectId": "myportfolio-8c965",
  "storageBucket": "myportfolio-8c965.firebasestorage.app",
  "messagingSenderId": "803778423074",
  "appId": "1:803778423074:web:0d4df1e9d25c8a05fa9d7b",
  "measurementId": "G-N98T7E8CFH",
  "databaseURL":"https://myportfolio-8c965-default-rtdb.firebaseio.com/"
}



# Initialize Firebase Admin SDK with credentials
cred = credentials.Certificate("service_account_key.json")  # Download this from Firebase Console
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://myportfolio-8c965-default-rtdb.firebaseio.com/'
})



# Admin login route
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



# Admin dashboard
@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/admin')
    data = db.reference('data').get()
    return render_template('admin_dashboard.html', data=data)

# Edit profile
@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if not session.get('admin'):
        return redirect('/admin')
    ref = db.reference('data')
    if request.method == 'POST':
        updated_data = {
            "name": request.form['name'],
            "title": request.form['title'],
            "teg_line": request.form['teg_line']
        }
        ref.update(updated_data)
        return redirect('/dashboard')
    data = ref.get()
    return render_template('edit_profile.html', data=data)

@app.route('/edit-skills', methods=['GET', 'POST'])
def edit_skills():
    if not session.get('admin'):
        return redirect('/admin')

    ref = db.reference('data')
    current_data = ref.get()
    skills = current_data.get('skills', [])

    if request.method == 'POST':
        if 'add' in request.form:
            new_skill = request.form['new_skill'].strip()
            if new_skill and new_skill not in skills:
                skills.append(new_skill)
        elif 'delete' in request.form:
            skill_to_delete = request.form['delete']
            skills = [s for s in skills if s != skill_to_delete]

        ref.update({'skills': skills})
        return redirect('/edit-skills')

    return render_template('edit_skills.html', data=current_data)


@app.route('/edit-languages', methods=['GET', 'POST'])
def edit_languages():
    if not session.get('admin'):
        return redirect('/admin')

    ref = db.reference('data')
    current_data = ref.get()
    languages = current_data.get('languages', {})

    if request.method == 'POST':
        # Update existing languages
        for lang in languages.keys():
            new_value = request.form.get(lang)
            if new_value is not None:
                languages[lang] = new_value

        # Add new language
        new_lang = request.form.get('new_language')
        new_percent = request.form.get('new_percentage')
        if new_lang and new_percent:
            languages[new_lang] = new_percent

        # Delete language
        if 'delete' in request.form:
            lang_to_delete = request.form['delete']
            if lang_to_delete in languages:
                del languages[lang_to_delete]

        ref.update({'languages': languages})
        return redirect('/edit-languages')

    return render_template('edit_languages.html', data=current_data)


@app.route('/edit-projects', methods=['GET', 'POST'])
def edit_projects():
    if not session.get('admin'):
        return redirect('/admin')

    ref = db.reference('data')
    data = ref.get()
    projects = data.get('projects', [])

    if request.method == 'POST':
        # Update count and review stats
        if 'update_counts' in request.form:
            ref.update({
                'no_of_completeprojects': request.form['no_of_completeprojects'],
                'positive_reviews': request.form['positive_reviews']
            })

        elif 'add_project' in request.form:
            new_project = {
                "project_name": request.form['project_name'],
                "Used_tech": request.form['used_tech'],
                "desciption": request.form['desciption'],
                "github_link": request.form['github_link']
            }
            projects.append(new_project)
            ref.update({'projects': projects})

        elif 'delete_index' in request.form:
            index = int(request.form['delete_index'])
            if 0 <= index < len(projects):
                projects.pop(index)
                ref.update({'projects': projects})

        return redirect('/edit-projects')

    return render_template('edit_projects.html', projects=projects, data=data)


@app.route('/edit-experience', methods=['GET', 'POST'])
def edit_experience():
    if not session.get('admin'):
        return redirect('/admin')

    ref = db.reference('data')
    data = ref.get()
    experiences = data.get('experiences', [])

    if request.method == 'POST':
        if 'add_experience' in request.form:
            new_exp = {
                "title": request.form['title'],
                "company_name": request.form['company_name'],
                "jobrole": request.form['jobrole'],
                "duration": request.form['duration'],
                "discription": request.form['discription']
            }
            experiences.append(new_exp)

        elif 'delete_index' in request.form:
            index = int(request.form['delete_index'])
            if 0 <= index < len(experiences):
                experiences.pop(index)

        ref.update({'experiences': experiences})
        return redirect('/edit-experience')

    return render_template('edit_experience.html', experiences=experiences)


@app.route('/edit-contact', methods=['GET', 'POST'])
def edit_contact():
    if not session.get('admin'):
        return redirect('/admin')

    ref = db.reference('data')
    data = ref.get()

    if request.method == 'POST':
        updated = {
            "email": request.form['email'],
            "location": request.form['location'],
            "mobile_no": request.form['mobile_no']
        }
        ref.update(updated)
        return redirect('/dashboard')

    return render_template('edit_contact.html', data=data)


@app.route('/edit-about', methods=['GET', 'POST'])
def edit_about():
    if not session.get('admin'):
        return redirect('/admin')

    ref = db.reference('data')
    data = ref.get()
    about_me = data.get('about_me', [])

    if request.method == 'POST':
        # Delete specific line
        if 'delete_index' in request.form:
            index = int(request.form['delete_index'])
            if 0 <= index < len(about_me):
                about_me.pop(index)

        else:
            # Save updated lines
            updated_about = []
            for i in range(len(about_me)):
                line = request.form.get(f'line_{i}', '').strip()
                if line:
                    updated_about.append(line)
            about_me = updated_about

            # Add new line
            new_line = request.form.get('new_line', '').strip()
            if new_line:
                about_me.append(new_line)

        ref.update({'about_me': about_me})
        return redirect('/edit-about')

    return render_template('edit_about.html', about_me=about_me)

@app.route('/edit-socials', methods=['GET', 'POST'])
def edit_socials():
    if not session.get('admin'):
        return redirect('/admin')

    ref = db.reference('data')
    data = ref.get()
    social_links = data.get('social_media_links', {})

    if request.method == 'POST':
        updated_links = {}
        for platform in social_links:
            new_link = request.form.get(platform, '').strip()
            updated_links[platform] = new_link
        ref.update({'social_media_links': updated_links})
        return redirect('/edit-socials')

    return render_template('edit_socials.html', social_links=social_links)


# Logout
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
    ref = db.reference('data')  # Path to your "data" node
    user_data = ref.get()
    return render_template("home.html", data=user_data)
    app.run(debug=True, port=1000, host='0.0.0.0')

@app.route('/')
def index():
    ref = db.reference('data')  # Path to your "data" node
    user_data = ref.get()
    return render_template("index.html", data=user_data)

if __name__=='__main__':
    app.run(debug=True, port=1000, host='0.0.0.0')