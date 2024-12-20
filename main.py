from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from database import db
from model import Users
from note import Note

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '1111'
db.init_app(app)


@app.route('/', methods = ('POST', 'GET'))
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 'dark_theme' not in session:
        session['dark_theme'] = False
    
    if request.method == 'POST':
        if request.form.get('create'):
            return redirect(url_for('create'))
        
        elif request.form.get('change-theme'):
            session['dark_theme'] = not session['dark_theme']
            user = Users.query.filter_by(username=session['username']).first()
            return render_template('index.html', notes = user.notes, shared_notes = user.shared_notes, username = session['username'], dark_theme = session['dark_theme'])
        
        elif request.form.get('logout'):
            session.pop('username')
            session.pop('user_id')
            return redirect(url_for('login'))
        
        else:
           for i in request.form.keys():    #obtaining note id
               session['currently_editing'] = i
               return redirect(url_for('edit'))
    
    user = Users.query.filter_by(username=session['username']).first()
    return render_template('index.html', notes = user.notes, shared_notes = user.shared_notes, username = session['username'], dark_theme = session['dark_theme'])


@app.route('/register', methods = ('POST', 'GET'))
def register():
    if 'dark_theme' not in session:
        session['dark_theme'] = False

    if request.method == 'POST':
        user = Users(username = request.form['username'], password = request.form['password'])
        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash('Такой пользователь уже существует.')
            return render_template('register.html', dark_theme = session['dark_theme'])
        session['username'] = user.username
        session['user_id'] = user.id
        return redirect(url_for('index'))

    return render_template('register.html', dark_theme = session['dark_theme'])


@app.route('/login', methods = ('POST', 'GET'))
def login():
    if 'dark_theme' not in session:
        session['dark_theme'] = False

    if request.method == 'POST':
        if request.form.get('submit'):
            user = Users.query.filter_by(username=request.form['username']).first()
            if user is None:
                flash('Такого пользователя не существует.')
                return render_template('login.html', dark_theme = session['dark_theme'])
            if request.form['password'] == user.password:
                session['username'] = request.form['username']
                session['user_id'] = user.id
                return redirect(url_for('index'))
        elif request.form.get('register'):
            return redirect(url_for('register'))

    return render_template('login.html', dark_theme = session['dark_theme'])


@app.route('/edit', methods = ('POST', 'GET'))
def edit():
    if 'currently_editing' not in session:
        return redirect(url_for('index'))

    if 'dark_theme' not in session:
        session['dark_theme'] = False

    if 'username' not in session or 'user_id' not in session:
        return redirect(url_for('login'))
    
    note = Note(id=session['currently_editing'])
    user = Users.query.filter_by(id=session['user_id']).first()
    if not (note.is_owner(session['user_id']) or user in note.get_users()):
        return redirect(url_for('login'))

    if request.method == 'POST':

        if request.form.get('return'):
            return redirect(url_for('index'))

        elif request.form.get('change-theme'):
            session['dark_theme'] = not session['dark_theme']
            user = Users.query.filter_by(username=session['username']).first()
            return render_template('edit.html', title = note.get_title(), text = note.get_text(), username = session['username'], dark_theme = session['dark_theme'])

        elif request.form.get('logout'):
            session.pop('username')
            session.pop('user_id')
            return redirect(url_for('login'))
        
        elif request.form.get('add_user') and request.form.get('username'):     
            if not note.is_owner(session['user_id']):
                return render_template('edit.html', title = note.get_title(), text = note.get_text(), dark_theme = session['dark_theme'], username = session['username'])
            user = Users.query.filter_by(username=request.form.get('username')).first()
            if user is not None:    
                if user not in note.get_users() and request.form.get('username') != session['username']:        
                    note.add_user(user)
                    flash(f'Пользователь {user.username} добавлен.')
            else:
                flash('Такого пользователя не существует.')
            
        elif request.form.get('delete'):
            if not note.is_owner(session['user_id']):
                return render_template('edit.html', title = note.get_title(), text = note.get_text(), dark_theme = session['dark_theme'], username = session['username'])
            session.pop('currently_editing')
            note.delete()
            return redirect(url_for('index'))
        
        elif request.form.get('text') or request.form.get('title'):
            note.set(title=request.form.get('title'), text=request.form.get('text'))
        
    return render_template('edit.html', title = note.get_title(), text = note.get_text(), dark_theme = session['dark_theme'], username = session['username'])


@app.route('/create', methods = ('POST', 'GET'))
def create():
    note = Note()
    note.create(created_by=session['user_id'])
    session['currently_editing'] = note.get_id()
    return redirect(url_for('edit'))
    

if __name__ == '__main__':
    app.run(debug=True)