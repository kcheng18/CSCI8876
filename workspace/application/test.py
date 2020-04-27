# def isInt(value):
#     try:
#         int(value)
#         return True
#     except ValueError:
#         return False

# x = input().lower()

# while True:
#     if x == 's' or x == 'm' or x == 'b':
#         break
#     print('Wrong')
#     x = input().lower()
    

# if x == 'x':
#     print(x)
# elif x == 'c':
#     print(x)
# elif isInt(x):
#     print('display')
# else:
#     print('Error')
# print(type(x))

# print(x.lower())

# if isInt(x):
#     print('OK')
# else:
#     print('Not OK')

import mysql.connector

def getResult(table, schemas, value):
    mycursor = mydb.cursor()
    if isinstance(value, str):
        value = '"{}"'.format(value)
    q = 'SELECT * FROM {} where {} = {}'.format(table, schemas, value)
    print(q)
    mycursor.execute(q)
    myresult = mycursor.fetchall()
    return myresult

mydb = mysql.connector.connect(
        host="127.0.0.1",       # host name
        user="kwoksuncheng",    # user id
        passwd="Test1234",      # user password
        database="test2"        # database name
)

def getkeywords(pmid):
    kids = getResult('search', 'pmid', pmid)
    if kids:
        print(kids)
        temp = []
        for kid in kids:
            temp.append(getResult('keywords', 'kid', kid[1])[0][1])
        return ', '.join(temp)
    else:
        return ''

pmid = 32216092
# keywords = getkeywords(pmid)
# print(keywords)

literature = getResult('literatures', 'pmid', pmid)
print(literature)
print(len(literature))