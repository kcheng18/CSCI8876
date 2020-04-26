import mysql.connector

mydb = mysql.connector.connect(
        host="127.0.0.1",       # host name
        user="kwoksuncheng",    # user id
        passwd="Test1234",      # user password
        database="bioi_project"        # database name
)

# checking if the data exists or not in relation table
def check_relation(table, schemas, values):
    mycursor = mydb.cursor()
    q = 'select * from {} where {}={} and {}={}'.format(table, schemas[0], values[0], schemas[1], values[1])
    mycursor.execute(q)
    myresult = mycursor.fetchall()
    return myresult

# Insertion for relation table
def insert_relation(table, schemas, values):
    mycursor = mydb.cursor()
    if not check_relation(table, schemas, values):
        temp = []
        for value in values:
            temp.append('%s')
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(table, ','.join(schemas), ','.join(temp)) # query for inertation
        val = tuple(values)         # inert values
        mycursor.execute(sql, val)  # executes the query
        mydb.commit()
        return True
    # print('already exist')
    return False                    # return false if the data already exist in DB

# checking if the data exists or not
def check(table, schema, value):
    mycursor = mydb.cursor()
    if isinstance(value,str):
        value = '"'+value+'"'
    q = 'select * from {} where {}={}'.format(table, schema, value)
    mycursor.execute(q)
    myresult = mycursor.fetchall()
    return myresult

# Inseting dat into the DB
def insert(table, schemas, values):
    mycursor = mydb.cursor()
    if not check(table, schemas[0],values[0]):
        temp = []
        for value in values:
            temp.append('%s')
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(table, ','.join(schemas), ','.join(temp)) # query for inertation
        val = tuple(values)             # inert values
        mycursor.execute(sql, val)      # executes the query
        mydb.commit()
        return True
    # print('already exist')
    return False                        # return false if the data already exist in DB

# Getting a literatures data and inset it into database
# data - | 0: PMID | 1: title | 2: date | 3: abs | 4: authors | 5: keywords | 
def insert_data(data):
    pmid = int(data[0])
    title = data[1] 
    date = data[2]
    ads = data[3]
    # -----------Checking if the literature exist in the DB or not before inseting another data ---------------
    if insert('literatures', ['pmid', 'title', 'date', 'abstract'], [pmid, title, date, ads]):

    # ----------- inserting authors into the authors table -----------------------------------------
        authors = data[4]
        for author in authors:
            name = author['name']
            insert('authors', ['name'], [name])
            aid = check('authors', 'name', name)
            if aid:
                insert_relation('written', ['pmid','aid'], [pmid,aid[0][0]])
    # ----------------------------------------------------------------------------------------------

    # ----------- inserting keywords into the keywords table ---------------------------------------
        keywords = data[5]
        for keyword in keywords:
            word = keyword['word']
            if '; ' in word:
                for w in word.split('; '):
                    insert('keywords', ['keyword'], [w])
                    kid = check('keywords', 'keyword', w)
                    if kid:
                        insert_relation('search', ['pmid','kid'], [pmid,kid[0][0]])
            else:
                insert('keywords', ['keyword'], [word])
                kid = check('keywords', 'keyword', word)
                if kid:
                    insert_relation('search', ['pmid','kid'], [pmid,kid[0][0]])
    # ------------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------------------