# notes.py



from flask import abort, make_response

from config import db
from models import Note, note_schema, carnet_schema
from models import Person, people_schema, person_schema


def read_all():
    carnet = Note.query.all()
    return carnet_schema.dump(carnet)

def read_one(noteid):
    note = Note.query.filter(Note.id == noteid).one_or_none()

    if note is not None:
        return note_schema.dump(note)
    else:
        abort(
            404, f"Note with id {noteid} not found"
        )