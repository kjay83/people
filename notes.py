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

def create(note):
    person_id = note.get("person_id")
    person = Person.query.get(person_id)

    if person:
        new_note = note_schema.load(note, session=db.session)
        person.notes.append(new_note)
        db.session.commit()
        return note_schema.dump(new_note), 201
    else:
        abort(
            404,
            f"Person not found for ID: {person_id}"
        )

def update(noteid, note):
    existing_note = Note.query.filter(Note.id == noteid).one_or_none()

    if existing_note:
        update_note = note_schema.load(note, session=db.session)
        existing_note.content = update_note.content
        db.session.merge(existing_note)
        db.session.commit()
        return note_schema.dump(existing_note), 201
    else:
        abort(
            404,
            f"Note with id {noteid} not found"
        )

def delete(noteid):
    existing_note = Note.query.get(noteid)

    if existing_note:
        db.session.delete(existing_note)
        db.session.commit()
        return make_response(f"{noteid} successfully deleted", 204)
    else:
        abort(404, f"Note with ID {noteid} not found")