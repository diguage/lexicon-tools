# coding=utf-8
# http://docs.sqlalchemy.org/en/latest/core/engines.html[Engine Configuration — SQLAlchemy 1.2 Documentation]
from sqlalchemy import create_engine
from sqlalchemy.sql import text

engine = create_engine('sqlite:///anki.sqlite')
conn = engine.connect()

fetchSql = text('''
                    SELECT
                      c.id   AS cid,
                      c.due  AS due,
                      n.id   AS nid,
                      n.sfld AS sfld,
                      n.flds AS flds
                    FROM cards c, notes n
                    WHERE c.did = 1508481220398 
                        AND n.flds LIKE '%margin%'
                    ORDER BY n.sfld
                '''
                )
notes = conn.execute(fetchSql).fetchall()

# http://docs.sqlalchemy.org/en/latest/core/connections.html[Working with Engines and Connections — SQLAlchemy 1.2 Documentation]
for note in notes:
    fields = note.flds.split("")
    print("%05d - %s\n" % (int(fields[-1]), note.flds))
    # try:
    #     trans = conn.begin()
    #     updateSql = text("UPDATE notes SET flds = :flds WHERE id = :id")
    #     conn.execute(updateSql, flds=note.flds.replace('world', ''), id=note.id)
    #     trans.commit()
    # except:
    #     trans.rollback()
    #     raise
conn.close
print("\n\ntask finish!!")
