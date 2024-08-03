from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from database import db
from model import Users, Notes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '1111'
db.init_app(app)

@app.route('/', methods = ('POST', 'GET'))
def index():
    return render_template('index.html')

@app.route('/register', methods = ('POST', 'GET'))
def register():
    if request.method == 'POST':
        user = Users(username = request.form['username'], password = request.form['password'])
        db.session.add(user)
        db.session.commit()

    return render_template('register.html')

@app.route('/login', methods = ('POST', 'GET'))
def login():
    if request.method == 'POST':
        try:
            user = Users.query.filter_by(username=request.form['username']).first()
        except:
            print('user not found')
        if request.form['password'] == user.password:
            session['user'] = request.form['username']
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/edit', methods = ('POST', 'GET'))
def edit():
    pass

if __name__ == '__main__':
    app.run(debug=True)