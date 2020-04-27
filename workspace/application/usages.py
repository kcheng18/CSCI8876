from selectDB import search, print_paperInfo
import topicmodeling

# getting user input and make a choice
def getInput(feature):
    print('-------------------- {} --------------------'.format(feature))
    print('Please enter the keyword you want to search: ')
    keyword = input()
    return search(keyword)

# check is intger or not
def isInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def check_input(user_input):
    while(user_input != 'x'):
        if user_input == '1':
            pmids = getInput('Papers search')
            print_paperInfo(pmids)                      # print the searching result
        elif user_input == '2':
            pmids = getInput('Topic Modeling')
            print('Enter the number of topic (1-20):')  # More number top may get bad result, so limiting lesser than 20
            numTop = input()
            while True:                          # check user input whether is integer and greater than 0 and lesser than 20 or not
                if isInt(numTop):
                    if int(numTop) > 0 and int(numTop) <= 20:
                        break
                print('Invalid number. Please enter again.')
            topicmodeling.run(int(numTop), pmids)       # start running topic modeling
        else:
            print('Wrong input. Please enter again.\n') # Input Error warning
        user_input = interface()

# user interface
def interface():
    print(  '[1]    Papers search\n' +
            '[2]    Topic Modeling\n' +
            '[X]    Exit\n' + 
            'Please enter your option: ')
    user_input = input()
    return user_input