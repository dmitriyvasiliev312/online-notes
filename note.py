from model import Notes
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

    def set(self, title : str | None, text : str | None):
        if title is not None and text is not None:
            self.__note.title = title
            self.__note.text = text
        elif title is not None:
            self.__note.title = title
        elif text is not None:
            self.__note.text = text
        if title is None and text is None:
            return
        print(self.__note.title)
        print(self.__note.text)
        db.session.commit()
    
    def create(self, created_by : int):
        self.__note = Notes(text = '', title = 'Новая заметка', created_by = created_by)
        db.session.add(self.__note)
        db.session.commit()

    def delete(self):
        db.session.delete(self.__note)
        db.session.commit()


            