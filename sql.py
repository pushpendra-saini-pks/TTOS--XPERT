import sqlite3

connection =sqlite3.connect("student.db")

## create a cursor object to insert records , create table , retrive information 
cursor = connection.cursor()


## creating a table 
table_info = """create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT );
"""

cursor.execute(table_info)

## insert some more records 

cursor.execute('''Insert Into STUDENT values('Alexander','AI','A',90)''')
cursor.execute('''Insert Into STUDENT values('Charlotte','AI','B',100)''')
cursor.execute('''Insert Into STUDENT values('James','Data Science','B',89)''')
cursor.execute('''Insert Into STUDENT values('Samuel','AI','A',75)''')
cursor.execute('''Insert Into STUDENT values('Victoria','Data Science','A',50)''')
cursor.execute('''Insert Into STUDENT values('Aria','Data Science','A',30)''')

## display all records 
print("The inserted records are ")

data = cursor.execute('''Select * From STUDENT''')

for row in data:
    print(row)
    
    
## close the connection 
connection.commit()
connection.close()