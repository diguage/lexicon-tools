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
                          AND c.queue = 0
                          AND c.nid = n.id
                    ORDER BY c.due
                '''
                )
notes = conn.execute(fetchSql).fetchall()

for note in notes:
    fields = note.flds.split("")
    r = int(fields[-1])
    if r > 11542:
        # # 调整 1w 单词以后的出现时间，1w后的单词四个月后再出现，
        # # 而且每个月只出现1000左右，每天33个。
        # TODO 这有可能不好搞。并不是按照 interval 来选词的
        # range = int(r / 1.1542)
        # count = range - 10000
        # n = count - int(count / 1000) * 1000
        # month = 30 * (int(range / 1000) - 7)
        # interval = month + int(n / 33)
        # # print(note.sfld, r, range, month, n, interval)

        # print("%s\t%s\t%17s\t%5d\t%5d" % (note.cid, note.nid, note.sfld, r, note.due))
        try:
            trans = conn.begin()
            updateSql = text("UPDATE cards SET due = :due WHERE id = :id")
            conn.execute(updateSql, due=(note.due + 20000), id=note.cid)
            trans.commit()
        except:
            trans.rollback()
            raise
conn.close
print("\n\ntask finish!!")
