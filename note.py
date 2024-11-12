from model import Notes, Users
from database import db

class Note():
    '''Create note object with id to edit the existing note, or without id to create an empty one and then use create() method to create a new note.'''
    def __init__(self, id : int | None = None):      
        if id is not None:
            self.__note = Notes.query.filter_by(id=id).first()

    def get_title(self) -> str:
        return self.__note.title

    def get_text(self) -> str:
        return self.__note.text
    
    def get_id(self) -> int:
        return self.__note.id

    def get_users(self) -> list[Users]:
        return self.__note.added_users

    def set(self, title : str | None, text : str | None):
        if title is not None and text is not None:
            self.__note.title = title
            self.__note.text = text
        elif title is not None:
            self.__note.title = title
        elif text is not None:
            self.__note.text = text
        else:
            return
        db.session.commit()
    
    def create(self, created_by : int):
        self.__note = Notes(text = '', title = 'Новая заметка', created_by = created_by)
        db.session.add(self.__note)
        db.session.commit()

    def delete(self):
        db.session.delete(self.__note)
        db.session.commit()

    def add_user(self, user : Users):
        self.__note.added_users.append(user)
        db.session.commit()

    def is_owner(self, user_id : int) -> bool:
        if self.__note.created_by == user_id:
            return True
        else:
            return False





            