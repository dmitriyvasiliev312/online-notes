from database import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(20))
    notes = db.relationship('Notes', backref = 'users')

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30))
    text = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
