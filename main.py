from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
import os

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')


# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL')

mail = Mail(app)


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        if not name or not email or not message:
            flash('Please fill out all fields.', 'error')
        else:
            msg = Message('New Contact Form Submission', recipients=[os.environ.get('EMAIL')])
            msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            mail.send(msg)

            flash('Your message has been sent!', 'success')

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
