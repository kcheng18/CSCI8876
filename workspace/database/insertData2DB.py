import json
import time
import os
from fileRW import readFile
from insert import insert_data

# A function for testing
def test():
    test_json = 'test.json'     # test file name
    data = readFile(test_json)
    articles = json.loads(data)
    for article in articles:
        temp = []
        for data in articles[article]:
            temp.append(articles[article][data])
        insert_data(temp)

if __name__ == "__main__":
    start_time = time.time()
    path = 'temp2'                  # the directory which contain datas with json format
    print('{}/{}'.format(0, len(os.listdir(path))))
    for index, filename in enumerate(os.listdir(path)):
        if filename.endswith('.json'):
            fullname = os.path.join(path, filename)
            data = readFile(fullname)
            articles = json.loads(data)
            for index2, article in enumerate(articles):
                print('From {}: {}/{}'.format(filename, index2+1, len(articles)))
                temp = []                                  
                for data in articles[article]:              # getting different datas from the article
                    temp.append(articles[article][data])    # saving those datas in the temp list
                insert_data(temp)                           # apply the temp list with datas to insertation
        print('Data list: {}/{}'.format(index+1, len(os.listdir(path))))
    print ('Running Time for inserting data: {} seconds'.format((time.time() - start_time)))