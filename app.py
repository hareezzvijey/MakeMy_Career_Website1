from flask import Flask, render_template,jsonify,request
from database import engine
from sqlalchemy import text
from werkzeug.utils import secure_filename
import os

app = Flask(__name__) # Create a Flask web server from the current module
    
def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))
        jobs = []
        for row in result.all():
            jobs.append(dict(row._mapping))
        return jobs

@app.route('/')
def hello_world():
    JOBS = load_jobs_from_db()
    return render_template('home.html',job = JOBS)

@app.route('/api/jobs')
def list_jobs():
    return jsonify(load_jobs_from_db())

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # Save to database
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO contacts (name, email, message) VALUES (:name, :email, :message)"),
                {"name": name, "email": email, "message": message}
            )
        print("Contact saved to database.")

        return render_template("contact.html", success=True)

    return render_template("contact.html", success=False)

UPLOAD_FOLDER = 'static/resumes'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/apply', methods=['GET', 'POST'])
def application():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cover = request.form['cover']
        file = request.files['resume']

        # Validate and save resume
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Save application to database
            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO applications (name, email, phone, resume, cover)
                    VALUES (:name, :email, :phone, :resume, :cover)
                """), {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "resume": filename,
                    "cover": cover
                })

            return render_template('application.html', success=True)
        else:
            return render_template('application.html', error="Invalid file format. Upload PDF, DOC, or DOCX.")

    return render_template('application.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')