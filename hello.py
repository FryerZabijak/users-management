from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/user/<int:user_id>')
def user(user_id):
    user = User.query.get(user_id)
    return render_template('user.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        user = User(username, email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users'))
    return render_template('register.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)