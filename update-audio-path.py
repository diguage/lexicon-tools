# http://docs.sqlalchemy.org/en/latest/core/engines.html[Engine Configuration — SQLAlchemy 1.2 Documentation]
from sqlalchemy import create_engine
from sqlalchemy.sql import text

engine = create_engine('sqlite:///collection.anki2')
conn = engine.connect()


# fetchSql = text("SELECT * FROM notes WHERE flds LIKE '%_1508301697368.mp3%' ORDER BY sfld")
fetchSql = text("SELECT * FROM notes WHERE flds LIKE '%]=%' ORDER BY sfld")
notes =  conn.execute(fetchSql).fetchall()

# http://docs.sqlalchemy.org/en/latest/core/connections.html[Working with Engines and Connections — SQLAlchemy 1.2 Documentation]
for note in notes:
    try:
        trans = conn.begin()
        updateSql = text("UPDATE notes SET flds = :flds WHERE id = :id")
        conn.execute(updateSql, flds=note.flds.replace("]=", "] = "), id=note.id)
        trans.commit()
    except:
        trans.rollback()
        raise
conn.close

print("OK")





