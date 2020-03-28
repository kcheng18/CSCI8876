import json
import time
import os
from fileRW import readFile
from insert import insert_data

if __name__ == "__main__":
    start_time = time.time()
    path = 'data'
    for index, filename in enumerate(os.listdir(path)):
        fullname = os.path.join(filename, path)
        data = readFile(fullname)
        articles = json.loads(data)
        for article in articles:
            temp = []
            for data in articles[article]:
                temp.append(articles[article][data])
            insert_data(temp)
    print ('Running Time for inserting data: {} seconds'.format((time.time() - start_time)))