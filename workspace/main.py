from fileRW import readFile, createfile
import ncbi
import time
import sys

start_time = time.time()
db = 'pubmed'
keyword = sys.argv[1].replace('_',' ')
numOfresult = int(sys.argv[2])
ncbi.efetch(keyword, db, numOfresult)
print ('Running Time for keyword - {}: {} seconds'.format(keyword, (time.time() - start_time)))