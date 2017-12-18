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
fetchSql = text("SELECT id, sfld, flds FROM notes WHERE mid = 1508301697368 ORDER BY sfld")
notes = conn.execute(fetchSql).fetchall()

# http://docs.sqlalchemy.org/en/latest/core/connections.html[Working with Engines and Connections — SQLAlchemy 1.2 Documentation]
for note in notes:
    wordListFileName = "./word-list.txt"
    wordListFile = open(wordListFileName, 'a', encoding="utf-8")
    fields = note.flds.split("")
    wordListFile.write("%05d - %s\n" % (int(fields[7]), note.flds))

    # jsonPath = "./dictionaries/english/" + note.sfld + ".json"
    # if os.path.exists(jsonPath):
    #     try:
    #         file = open(jsonPath, 'r', encoding="utf-8")
    #         dict = json.loads(file.readline())
    #         meaning = []
    #         if "basic" in dict:
    #             meaning += dict["basic"]["explains"]
    #
    #         if "web" in dict:
    #             for w in dict["web"]:
    #                 meaning.append("[W](%s)%s" % (w["key"], ",".join(w["value"])))
    #         if "translation" in dict:
    #             meaning.append("[T]%s" % ",".join(dict['translation']))
    #
    #         fields = note.flds.split("")
    #         fields[3] = "<ul><li>%s</li></ul>" % "</li><li>".join(meaning)
    #         # print(note.id," -- ", )
    #
    #         try:
    #             trans = conn.begin()
    #             updateSql = text("UPDATE notes SET flds = :flds WHERE mid = 1508301697368 AND id = :id")
    #             conn.execute(updateSql, flds="".join(fields), id=note.id)
    #             trans.commit()
    #         except:
    #             trans.rollback()
    #             raise
    #
    #     finally:
    #         file.close()
    # else:
    #     print(note.sfld)

conn.close
wordListFile.close()
print("\n\ntask finish!!")
