import mysql.connector

mydb = mysql.connector.connect(
        host="127.0.0.1",       # host name
        user="kwoksuncheng",    # user id
        passwd="Test1234",      # user password
        database="test2"        # database name
)

def getauthors(pmid):
    aids = getResult('written', 'pmid', pmid)
    if aids:
        temp = []
        for aid in aids:
            temp.append(getResult('authors', 'aid', aid[1])[0][1])
        return ', '.join(temp)
    else:
        return ''

def getkeywords(pmid):
    kids = getResult('search', 'pmid', pmid)
    if kids:
        temp = []
        for kid in kids:
            temp.append(getResult('keywords', 'kid', kid[1])[0][1])
        return ', '.join(temp)
    else:
        return ''

def isInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def print_handing(option):
    if option == 1:
        print('|    Pmid\t|\t\ttitle\t\t|   Pub_date\t|')

def getResult(table, schemas, value):
    mycursor = mydb.cursor()
    if isinstance(value, str):
        value = '"{}"'.format(value)
    q = 'SELECT * FROM {} where {} = {}'.format(table, schemas, value)
    mycursor.execute(q)
    myresult = mycursor.fetchall()
    return myresult

def getData(datas, index):
    temp = []
    for data in datas:
        temp.append(data[index])
    return ', '.join(temp)

def search(keyword):
    kid = getResult('keywords', 'keyword', keyword)
    if kid:
        pmids = getResult('search', 'kid', kid[0][0])
        return pmids

def display(pmid):
    literature = getResult('literatures', 'pmid', pmid)
    if literature:
        keywords = getkeywords(pmid)
        authors = getauthors(pmid)
        print(  '\nPMID:     {}\n\n'.format(pmid) +
                'Pub_date: {}\n\n'.format(literature[0][3]) +
                'Tilte:    {}\n\n'.format(literature[0][1]) + 
                'Authors:  {}\n\n'.format(authors) +
                'Abstract:\n{}\n\n'.format(literature[0][2]) +
                'Keywords: {}\n'.format(keywords))
        print('Enter [S]earch another paper | [B]ack to the search page | [M]ain menu')
        display_input = input().lower()
        while True:
            if display_input == 's' or display_input == 'b' or display_input == 'm':
                return display_input
            print("Invalid Input. Please enter again.")
            display_input = input().lower()
    else:
        print('Paper not found')
        return 'b'
            
def searchChoice(counter, size, i):
    style = ['[C] see more papers | ', '']
    print('{}/{}'.format(counter, size))
    print("\nEnter pmid see paper's detail | {}[B]ack to the main menu".format(style[i]))
    user_input = input().lower()
    while True:
        if (user_input == 'b' or user_input == 'c' or isInt(user_input) and i == 0) or (user_input == 'b' or isInt(user_input) and i == 1):
            break
        print('Invalid Input. Please enter again.')
        user_input = input().lower()
    return user_input

def display_decision(choice, counter, size, i):
    display_input = display(choice)
    while True:
        if display_input == 'm':
            break
        elif display_input == 'b':
            choice = searchChoice(counter, size, i)
        elif display_input == 's':
            print('Please enter pmid:')
            choice = input()
        if choice != 'b' and choice != 'c':
            display_input = display(choice)
        else:
            break

def print_paperInfo(pmids):
    if pmids:
        size_pimds = len(pmids)
        print('\n{} Found'.format(size_pimds))
        print_handing(1)
        for index, pmid in enumerate(pmids):
            myresult = getResult('literatures', 'pmid', pmid[0])
            temp = '|   {}\t| {} |  {}\t|'.format(myresult[0][0],myresult[0][1][0:26] + '...',myresult[0][3])
            print(temp)
            if (index+1)%10 == 0:
                choice = searchChoice(index+1, size_pimds, 0)
                if choice == 'b':
                    break
                elif choice == 'c':
                    continue
                else:
                    display_decision(choice, index+1, size_pimds, 0)
        choice = searchChoice(index+1, size_pimds, 1)
        if choice != 'b':
            display_decision(choice, index+1, size_pimds, 1)
    else:
        print('\nNo result found\n')