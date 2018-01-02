# coding=utf-8
# http://docs.sqlalchemy.org/en/latest/core/engines.html[Engine Configuration — SQLAlchemy 1.2 Documentation]
import os
import ujson as json
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
                    ORDER BY n.sfld
                '''
                )
notes = conn.execute(fetchSql).fetchall()

# http://docs.sqlalchemy.org/en/latest/core/connections.html[Working with Engines and Connections — SQLAlchemy 1.2 Documentation]
for note in notes:
    jsonPath = "./dictionaries/english/" + note.sfld + ".json"
    if os.path.exists(jsonPath):
        try:
            file = open(jsonPath, 'r', encoding="utf-8")
            dict = json.loads(file.readline())
            meaning = []
            if "basic" in dict:
                meaning += dict["basic"]["explains"]

            if "web" in dict:
                for w in dict["web"]:
                    meaning.append("[W](%s)%s" % (w["key"], ",".join(w["value"])))
            if "translation" in dict: # TODO 感觉这个可以不要
                meaning.append("[T]%s" % ",".join(dict['translation']))

            fields = note.flds.split("")
            fields[3] = "<ul><li>%s</li></ul>" % "</li><li>".join(meaning)

            try:
                trans = conn.begin()
                updateSql = text("UPDATE notes SET flds = :flds WHERE mid = 1508301697368 AND id = :id")
                conn.execute(updateSql, flds="".join(fields), id=note.id)
                trans.commit()
            except:
                trans.rollback()
                raise

        finally:
            file.close()
    else:
        print(note.sfld)
conn.close
print("\n\ntask finish!!")
