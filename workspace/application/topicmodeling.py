import topMod_lemm as topmod
from selectDB import search
from fileRW import readFile

def isInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def displayOption(conter, size, style):
    print('\n{}/{}'.format(conter, size))
    styles = ['[N]ext page for more papers | ', '']
    print("\nEnter topic number to see more terms | {}[B]ack to the main menu".format(styles[style]))
    user_input = input().lower()
    while True:
        if user_input == 'b' or isInt(user_input) or (style == 0 and user_input == 'n'):
            if isInt(user_input):
                if int(user_input) > size:
                    print(user_input)
                    print(type(user_input))
                    break
            break
        print('Invalid Input. Please enter again.')
        user_input = input().lower()
    return user_input

def displaytopic(top_list, user_input):
    select_top = top_list[int(user_input)]
    top_words = select_top.split(',')
    print('\nTopic {}: \n'.format(user_input))
    temp = []
    for index, word in enumerate(top_words):
        temp.append(word)
        if (index+1)%5 == 0:
            print('{}'.format('\t\t'.join(temp)))
            temp = []
    print('Enter [S]ee another topic | [B]ack to the topic result page | [M]ain menu')
    display_input = input().lower()
    while True:
        if display_input == 's' or display_input == 'b' or display_input == 'm':
            break
        print("Invalid Input. Please enter again.")
        display_input = input().lower()
    if display_input == 's':
        print('Please enter topic number:')
        top = input()
        displaytopic(top_list, top)
    else:
        return display_input
    
# Display topic modeling result with top 5 terms from the topic
def display():
    print('|    Topic\t|\t\tTerms (Top 5)\t\t\t\t|')
    result = readFile('./topicmodeling/topics.txt')
    size = len(result.split('\n'))
    theEnd = False
    for index, sent in enumerate(result.split('\n')):
        topic = 'Topic {}'.format(index+1)
        top_words = sent.split(',')
        print('|    {}\t|  {}'.format(topic, ', '.join(top_words[0:5])))
        if (index+1)%10 == 0 and index+1 < size:
            user_input = displayOption(index+1, size, 0)
            if user_input == 'b':
                break
            elif user_input == 'n':
                print('|    Topic\t|\t\tTerms (Top 5)\t\t\t\t|')
                continue
            else:
                display_input = displaytopic(result.split('\n'), user_input)
                if display_input == 'm':
                    break
            print('|    Topic\t|\t\tTerms (Top 5)\t\t\t\t|')
        if index+1 == size:
            theEnd = True
    if theEnd:
        display_input_last = ''
        user_input_last = ''
        while True:
            if display_input_last == 'm' or user_input_last == 'b':
                break
            user_input_last = displayOption(index+1, size,1)
            if isInt(user_input_last):
                display_input_last = displaytopic(result.split('\n'), user_input_last)

def run(num_topics, pmid):
    topmod.run(num_topics, 100, 1000, pmid)
    display()

# if __name__ == "__main__":
#     pmid = search('biofilm')
#     run(10, pmid)