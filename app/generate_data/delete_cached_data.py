# In this script, we will be connecting to the Database. The DB Path to be provided by Flask App. The Tablename to be provided by the App.
# All the records with LAST_UPDATE_DATE < CURRENT_DAY - 5 will be purged from the db.
import sqlite3, os
from datetime import datetime, timedelta

# os.chdir(r'C:\Users\ahussainm\Documents\Python\Projects\Online_Shopping_Proj2\web_app')

print("These rows eed to be delete ")
# conn = sqlite3.connect('test1.db')
# select_st = f"""SELECT last_update_date FROM RESULTS WHERE date(last_update_date) < date('now','-5 day');"""
# cursor = conn.execute(select_st)

# for row in cursor:
# 	print(row)

