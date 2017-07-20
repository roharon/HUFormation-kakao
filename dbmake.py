import sqlite3

con = sqlite3.connect("./DB/userdata.db")
cur = con.cursor()
cur.execute("CREATE TABLE user_data(Name TEXT, Campus TEXT);")


print("DataBase | CREATE TABLE, DONE.")
