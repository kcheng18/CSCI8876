from selectDB import search, print_paperInfo

def check_input(user_input):
    while(user_input != 'x'):
        if user_input == '1':
            print('Papers search')
            print('Please enter the keyword you want to search: ')
            keyword = input()
            pmids = search(keyword)
            print_paperInfo(pmids)
        elif user_input == '2':
            print('Topic Modeling')
        else:
            print('Wrong input. Please enter again.\n')
        user_input = interface()

def interface():
    print(  '[1]    Papers search\n' +
            '[2]    Topic Modeling\n' +
            '[X]    Exit\n' + 
            'Please enter your option: ')
    user_input = input()
    return user_input