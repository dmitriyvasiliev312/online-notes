from database import db

user_note = db.Table('user_note',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),   
    db.Column('note_id', db.Integer, db.ForeignKey('notes.id'))              
)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(20))
    notes = db.relationship('Notes', backref = 'users')
    shared_notes = db.relationship('Notes', secondary=user_note, back_populates='added_users')

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30))
    text = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    added_users = db.relationship('Users', secondary=user_note, back_populates='shared_notes')
