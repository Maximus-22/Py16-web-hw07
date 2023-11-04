from sqlalchemy import select

from connect_db import session
from models import Note, Tag, Record, note_m2m_tag

if __name__ == '__main__':
    query_1 = session.execute(
        select(Note.id, Note.name, Record.description, Record.done, Tag.name.label('tag'))
        .join(Record)
        .join(note_m2m_tag)
        .join(Tag).filter(Tag.name == 'food')
          ).mappings().all()

    print(*query_1, sep = "\n")