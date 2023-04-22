import sqlite3
import csv

dbname = input()
table = input().split()
table1 = table[0]
table2 = table[1]
n = int(input())
a = []

con = sqlite3.connect(dbname)
cur = con.cursor()

result = cur.execute(f"""SELECT designation FROM {table1} WHERE {table2} >= {n}""").fetchall()
result1 = cur.execute(f"""SELECT const_id FROM stars WHERE designation = '{result[0][0]}'""").fetchall()
result3 = cur.execute(f"""SELECT name FROM constellations WHERE id = '{result1[0][0]}""")
result4 = cur.execute(f"""SELECT distance FROM stars WHERE  designation = '{result[0][0]}""").fetchall()
result5 = cur.execute(f"""SELECT first FROM stars WHERE  designation = '{result[0][0]}""").fetchall()
result6 = cur.execute(f"""SELECT designation FROM elements WHERE  id = '{result1[0][0]}""").fetchall()
result7 = cur.execute(f"""SELECT first FROM stars WHERE  designation = '{result[0][0]}""").fetchall()

con.close()
