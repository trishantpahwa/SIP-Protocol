import sys
sys.path.insert(0, 'C:\\Users\\R&DTrainee3\\Desktop\\SIP-Protocol\\src')
import database

db = database.database()
query = db.create_table()
print(db.execute_statement(query))
