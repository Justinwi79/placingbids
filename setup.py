"""
Name: Harold Justin Windham
Date: 10/23/2022
Assignment: Module 8: Send Authenticated Message
Due Date: 10/23/2022
About this project: This script authenticates messages sent in browser
Assumptions: N/A
All work below was performed by Harold Justin Windham
"""

"""
References: Dr. Works modules and videos. 
"""

import sqlite3
import Encryption

#create new db
conn = sqlite3.connect('FlaskDB.db')

# create Cursor to execute queries
cur = conn.cursor()


# drop table from database
try:
    conn.execute('''Drop table Bidder''')
    # save changes
    conn.commit()
    print('Bidder table dropped.')
except:
    print('Bidder table did not exist')


# create table in database
cur.execute('''CREATE TABLE Bidder(
BidderId INTEGER PRIMARY KEY NOT NULL,
Name TEXT NOT NULL,
PhoneNumber TEXT NOT NULL,
PrequalifiedUpperLimit Decimal(12,2) NOT NULL,
AppRoleLevel INTEGER NOT NULL,
LoginPassword TEXT NOT NULL);
''')

# save changes
conn.commit()
print('Bidder Table created.')


Nm = str(Encryption.cipher.encrypt(b'James Bond').decode("utf-8"))
PhNum = str(Encryption.cipher.encrypt(b'111-222-0007').decode("utf-8"))
Pwd = str(Encryption.cipher.encrypt(b'test123').decode("utf-8"))

cur.execute('''Insert Into Bidder ('Name','PhoneNumber','PrequalifiedUpperLimit','AppRoleLevel','LoginPassword') 
Values (?,?,?,?,?);''',(Nm, PhNum, 300000,3, Pwd))
conn.commit()

Nm = str(Encryption.cipher.encrypt(b'Tina Whitefield').decode("utf-8"))
PhNum = str(Encryption.cipher.encrypt(b'333-444-5555').decode("utf-8"))
Pwd = str(Encryption.cipher.encrypt(b'test456').decode("utf-8"))

cur.execute('''Insert Into Bidder ('Name','PhoneNumber','PrequalifiedUpperLimit','AppRoleLevel','LoginPassword') 
Values (?,?,?,?,?);''',(Nm, PhNum, 2500000,2, Pwd))
conn.commit()

Nm = str(Encryption.cipher.encrypt(b'Tim Jones').decode("utf-8"))
PhNum = str(Encryption.cipher.encrypt(b'777-888-9999').decode("utf-8"))
Pwd = str(Encryption.cipher.encrypt(b'test789').decode("utf-8"))

cur.execute('''Insert Into Bidder ('Name','PhoneNumber','PrequalifiedUpperLimit','AppRoleLevel','LoginPassword') 
Values (?,?,?,?,?);''',(Nm, PhNum, 125000,1, Pwd))
conn.commit()

Nm = str(Encryption.cipher.encrypt(b'Jenny Smith').decode("utf-8"))
PhNum = str(Encryption.cipher.encrypt(b'3333-222-1111').decode("utf-8"))
Pwd = str(Encryption.cipher.encrypt(b'test321').decode("utf-8"))

cur.execute('''Insert Into Bidder ('Name','PhoneNumber','PrequalifiedUpperLimit','AppRoleLevel','LoginPassword') 
Values (?,?,?,?,?);''',(Nm, PhNum, 10000,2, Pwd))
conn.commit()

Nm = str(Encryption.cipher.encrypt(b'Mike Hatfield').decode("utf-8"))
PhNum = str(Encryption.cipher.encrypt(b'555-444-3333').decode("utf-8"))
Pwd = str(Encryption.cipher.encrypt(b'test654').decode("utf-8"))

cur.execute('''Insert Into Bidder ('Name','PhoneNumber','PrequalifiedUpperLimit','AppRoleLevel','LoginPassword') 
Values (?,?,?,?,?);''',(Nm, PhNum, 2500,1, Pwd))
conn.commit()

Nm = str(Encryption.cipher.encrypt(b'Steve Makers').decode("utf-8"))
PhNum = str(Encryption.cipher.encrypt(b'999-888-7777').decode("utf-8"))
Pwd = str(Encryption.cipher.encrypt(b'test987').decode("utf-8"))

cur.execute('''Insert Into Bidder ('Name','PhoneNumber','PrequalifiedUpperLimit','AppRoleLevel','LoginPassword') 
Values (?,?,?,?,?);''',(Nm, PhNum, 750,3, Pwd))
conn.commit()

# iterate over the rows
for row in cur.execute('SELECT * FROM Bidder;'):
    print(row)


# close database connection
conn.close()
print('Connection closed.')
