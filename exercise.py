from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'quiz_6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///startup_db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Startup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    question1 = db.Column(db.String(150), nullable=False)
    question2 = db.Column(db.String(150), nullable=False)

    def __str__(self):
        return f'User Name:{self.name}; Surname: {self.surname}; \n' \
               f' Question1: {self.question1}; Question2: {self.question2}'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        session['name'] = user
        return redirect(url_for('user'))
    else:
        if 'user' in request.args:
            user = request.args['user']
        return render_template('login.html')


@app.route('/user')
def user():
    if 'name' in session:
        return f"გამარჯობა {session['name']}"
    else:
        return redirect(url_for('login'))


@app.route('/startup', methods=['GET', 'POST'])
def startup():
    if request.method == 'POST':
        n = request.form['name']
        s = request.form['surname']
        q1 = request.form['question1']
        q2 = request.form['question2']

        if n == '' or s == '' or q1 == '' or q2 == '':
            flash('შეიყვანეთ ყველა მონაცემი', 'error')
        else:
            b1 = Startup(name=n, surname=s, question1=q1, question2=q2)
            db.session.add(b1)
            db.session.commit()
            flash('მონაცემები დამატებულია', 'info')

    return render_template('sql.html')


@app.route('/logout')
def logout():
    session.pop('name', None)
    return 'you are logged out'


if __name__ == '__main__':
    app.run(debug=True)
