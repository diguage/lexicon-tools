# coding=utf-8
# http://docs.sqlalchemy.org/en/latest/core/engines.html[Engine Configuration — SQLAlchemy 1.2 Documentation]
import os
import ujson as json
from sqlalchemy import create_engine
from sqlalchemy.sql import text

engine = create_engine('sqlite:///anki.sqlite')
conn = engine.connect()

# fetchSql = text("SELECT * FROM notes WHERE flds LIKE '%_1508301697368.mp3%' ORDER BY sfld")
# fetchSql = text("SELECT * FROM notes WHERE flds LIKE '%]=%' ORDER BY sfld")
# fetchSql = text("SELECT id, sfld, flds FROM notes WHERE mid = 1508301697368 ORDER BY sfld")
# fetchSql = text("SELECT id, sfld, flds FROM notes WHERE mid = 1508301697368 AND flds LIKE  '%margin%' ORDER BY sfld")
fetchSql = text('''
                    SELECT
                      c.id   AS cid,
                      c.due  AS due,
                      n.id   AS nid,
                      n.sfld AS sfld,
                      n.flds AS flds
                    FROM cards c, notes n
                    WHERE c.did = 1508481220398 
                    ORDER BY n.sfld
                '''
                )
notes = conn.execute(fetchSql).fetchall()

# http://docs.sqlalchemy.org/en/latest/core/connections.html[Working with Engines and Connections — SQLAlchemy 1.2 Documentation]
for note in notes:
    wordListFileName = "./word-list.txt"
    wordListFile = open(wordListFileName, 'a', encoding="utf-8")
    fields = note.flds.split("")
    wordListFile.write("%05d - %s\n" % (int(fields[-1]), note.flds))
    wordListFile.close()
conn.close
print("\n\ntask finish!!")
