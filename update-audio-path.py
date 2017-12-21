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
fetchSql = text(
    "SELECT  c.id   AS id,  n.sfld AS sfld,  n.flds AS flds FROM notes AS n, cards AS c WHERE c.nid = n.id AND c.ivl = 0 AND c.did = 1508481220398")
notes = conn.execute(fetchSql).fetchall()

# http://docs.sqlalchemy.org/en/latest/core/connections.html[Working with Engines and Connections — SQLAlchemy 1.2 Documentation]
for note in notes:
    # wordListFileName = "./word-list.txt"
    # wordListFile = open(wordListFileName, 'a', encoding="utf-8")
    # fields = note.flds.split("")
    # wordListFile.write("%05d - %s\n" % (int(fields[7]), note.flds))
    # wordListFile.close()

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

    # try:
    #     trans = conn.begin()
    #     updateSql = text("UPDATE notes SET flds = :flds WHERE mid = 1508301697368 AND id = :id")
    #     conn.execute(updateSql, flds=note.flds.replace(' style="margin-left: 20px; "', ""), id=note.id)
    #     trans.commit()
    # except:
    #     trans.rollback()
    #     raise

    fields = note.flds.split("")
    r = int(fields[-1])
    if r > 11542:
        # 调整 1w 单词以后的出现时间，1w后的单词四个月后再出现，
        # 而且每个月只出现1000左右，每天33个。
        range = int(r / 1.1542)
        count = range - 10000
        n = count - int(count / 1000) * 1000
        month = 30 * (int(range / 1000) - 7)
        interval = month + int(n / 33)
        # print(note.sfld, r, range, month, n, interval)
        print("%03d" % interval, note.sfld, r, range, month, n)
        try:
            trans = conn.begin()
            updateSql = text("UPDATE cards SET ivl = :ivl WHERE id = :id")
            conn.execute(updateSql, ivl=interval, id=note.id)
            trans.commit()
        except:
            trans.rollback()
            raise

conn.close
print("\n\ntask finish!!")
