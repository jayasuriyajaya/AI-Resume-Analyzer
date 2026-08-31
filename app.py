from flask import Flask, render_template, session, redirect, url_for

from routes.auth import auth_bp
from routes.resume import resume_bp


app = Flask(__name__)

app.secret_key = "change-this-secret-key"

app.register_blueprint(auth_bp)
app.register_blueprint(resume_bp)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)