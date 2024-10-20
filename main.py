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
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if request.form.get('create'):
            return redirect(url_for('create'))
        if request.form.get('logout'):
            session.pop('user')
            return redirect(url_for('login'))
        else:
           for i in request.form.keys():    #obtaining note id
               session['currently_editing'] = i
               return redirect(url_for('edit'))
    
    user = Users.query.filter_by(username=session['user']).first()
    return render_template('index.html', notes = user.notes, username = session['user'])

@app.route('/register', methods = ('POST', 'GET'))
def register():
    if request.method == 'POST':
        user = Users(username = request.form['username'], password = request.form['password'])
        db.session.add(user)
        db.session.commit()
        session['user'] = request.form['username']
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods = ('POST', 'GET'))
def login():
    if request.method == 'POST':
        if request.form.get('submit'):
            try:
                user = Users.query.filter_by(username=request.form['username']).first()
            except:
                print('user not found')
            if request.form['password'] == user.password:
                session['user'] = request.form['username']
                return redirect(url_for('index'))
        elif request.form.get('register'):
            return redirect(url_for('register'))

    return render_template('login.html')

@app.route('/edit', methods = ('POST', 'GET'))
def edit():
    if 'currently_editing' not in session:
        return redirect(url_for('index'))
    
    note = Notes.query.filter_by(id=session['currently_editing']).first()
    if request.method == 'POST':
        if request.form.get('return'):
            session.pop('currently_editing')
            return redirect(url_for('index'))
        if request.form.get('text') and request.form.get('title'):
            note.text = request.form.get('text')
            note.title = request.form.get('title')
            db.session.commit()
            return render_template('edit.html', note = Notes(title = request.form.get('title'), text = request.form.get('text'))) #returning note with changed text and title, not to querry db again      
        elif request.form.get('text'):
            note.text = request.form.get('text')
            db.session.commit()
            return render_template('edit.html', note = Notes(title = note.title, text = request.form.get('text')))
        elif request.form.get('title'):
            note.title = request.form.get('title')
            db.session.commit()
            return render_template('edit.html', note = Notes(title = request.form.get('title'), text = note.title))

    return render_template('edit.html', note = note)

@app.route('/create', methods = ('POST', 'GET'))
def create():
    user = Users.query.filter_by(username=session['user']).first()
    note = Notes(text = '', title = 'Новая заметка', created_by = user.id)
    db.session.add(note)
    db.session.commit()
    session['currently_editing'] = note.id
    return redirect(url_for('edit'))
    

if __name__ == '__main__':
    app.run(debug=True)