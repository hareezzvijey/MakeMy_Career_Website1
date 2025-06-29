from flask import Flask, render_template,jsonify,request
from database import engine
from sqlalchemy import text

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
        print(f"Contact received from {name} ({email}): {message}")
        return render_template("contact.html", success=True)
    return render_template("contact.html", success=False)

@app.route('/apply', methods=['GET', 'POST'])
def application():
    if request.method == 'POST':
        return "Application Submitted!"
    return render_template('application.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
