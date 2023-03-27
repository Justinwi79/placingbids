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

#create new db
conn = sqlite3.connect('SilentAuction.db')

# create Cursor to execute queries
cur = conn.cursor()


# drop table from database
try:
    conn.execute('''Drop table AuctionItem''')
    # save changes
    conn.commit()
    print('AuctionItem table dropped.')
except:
    print('AuctionItem table did not exist')


# create table in database
cur.execute('''CREATE TABLE AuctionItem(
ItemId INTEGER PRIMARY KEY NOT NULL,
ItemName TEXT NOT NULL,
ItemDesc TEXT NOT NULL,
LowerBidLimit Decimal(12,2) NOT NULL,
HighestBidderId INTEGER NULL,
HighestBidAmnt Decimal(12,2) NULL);
''')

# save changes
conn.commit()
print('AuctionItem Table created.')


cur.execute('''Insert Into AuctionItem ('ItemName','ItemDesc','LowerBidLimit','HighestBidderId','HighestBidAmnt') 
Values (?,?,?,NULL,NULL);''',('Picasso Painting', 'Science and Charity, painted in 1897 ', 300000))
conn.commit()

cur.execute('''Insert Into AuctionItem ('ItemName','ItemDesc','LowerBidLimit','HighestBidderId','HighestBidAmnt') 
Values (?,?,?,NULL,NULL);''',('Old socks', 'a pair of old socks', 3))
conn.commit()

cur.execute('''Insert Into AuctionItem ('ItemName','ItemDesc','LowerBidLimit','HighestBidderId','HighestBidAmnt') 
Values (?,?,?,?,?);''',('Tiffany & Co Bracelet', '14k GOLD and TURQUOISE HINGED BANGLE BRACELET', 1000,1,200))
conn.commit()

cur.execute('''Insert Into AuctionItem ('ItemName','ItemDesc','LowerBidLimit','HighestBidderId','HighestBidAmnt') 
Values (?,?,?,?,?);''',('An English mahogany quarter chiming tall case clock', 'An English mahogany quarter chiming tall case clock, J.C. Jennens & Son, London, late 19th / early 20th century', 500,2,1500))
conn.commit()

cur.execute('''Insert Into AuctionItem ('ItemName','ItemDesc','LowerBidLimit','HighestBidderId','HighestBidAmnt') 
Values (?,?,?,?,?);''',('Steuben Vase', 'Steuben aurene glass vase 8"h. Signed on base aurene 541. Good condition.', 50,4,25))
conn.commit()


# iterate over the rows
for row in cur.execute('SELECT * FROM AuctionItem;'):
    print(row)


# close database connection
conn.close()
print('Connection closed.')
