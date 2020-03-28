import mysql.connector

mydb = mysql.connector.connect(
        host="127.0.0.1",   # host name
        user="kwoksuncheng",    # user id
        passwd="Test1234",  # user password
        database="test2"    # database name
)

# checking if the data exists or not in relation table
def check_relation(mycursor, table, schemas, values):
    q = 'select * from {} where {}={} and {}={}'.format(table, schemas[0], values[0], schemas[1], values[1])
    mycursor.execute(q)
    return mycursor.fetchone() 

# Insertion for relation table
def insert_relation(mycursor,table, schemas, values):
    if not check_relation(mycursor, table, schemas, values):
        temp = []
        for value in values:
            temp.append('%s')
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(table, ','.join(schemas), ','.join(temp)) # query for inertation
        val = tuple(values)    # inert values
        mycursor.execute(sql, val)  # executes the query
        mydb.commit()
        return True
    print('already exist')
    return False # return false if the data already exist in DB

# checking if the data exists or not
def check(mycursor, table, schema, value):
    if isinstance(value,str):
        value = '"'+value+'"'
    q = 'select * from {} where {}={}'.format(table, schema, value)
    mycursor.execute(q)
    return mycursor.fetchone() 

# Inseting dat into the DB
def insert(mycursor,table, schemas, values):
    if not check(mycursor, table, schemas[0],values[0]):
        temp = []
        for value in values:
            temp.append('%s')
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(table, ','.join(schemas), ','.join(temp)) # query for inertation
        val = tuple(values)    # inert values
        mycursor.execute(sql, val)  # executes the query
        mydb.commit()
        return True
    print('already exist')
    return False # return false if the data already exist in DB

# Getting a literatures data and inset it into database
# data - | 0: PMID | 1: title | 2: date | 3: abs | 4: authors | 5: keywords | 
def insert_data(data):
    mycursor = mydb.cursor()

    pmid = int(data[0])
    title = data[1]
    ads = data[2]  
    # # date = data[2]
    # # ads = data[3]
    # # if insert(mycursor,'literatures', ['pmid', 'title', 'date', 'abstract'], [pmid, title, date, ads]):
    
    # -----------Checking if the literature exist in the DB or not before inseting another data ----
    if insert(mycursor,'literatures', ['pmid', 'title', 'abstract'], [pmid, title, ads]):
    #   authors = data[4]
    #   keywords = data[5]

    # ----------- inserting authors into the authors table -----------------------------------------
        authors = data[3]
        for author in authors:
            name = author['name']
            insert(mycursor,'authors', ['name'], [name])
            aid = int(check(mycursor,'authors', 'name', name)[0])
            insert_relation(mycursor,'written', ['pmid','aid'], [pmid,aid])
    # ----------------------------------------------------------------------------------------------

    # ----------- inserting keywords into the keywords table ---------------------------------------
        keywords = data[4]
        for keyword in keywords:
            word = keyword['word']
            insert(mycursor,'keywords', ['keyword'], [word])
            kid = int(check(mycursor,'keywords', 'keyword', word)[0])
            insert_relation(mycursor,'search', ['pmid','kid'], [pmid,kid])
    # ----------------------------------------------------------------------------------------------