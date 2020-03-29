from fileRW import readFile, createfile, createfileb
import getdata_json as gd
import xml.etree.ElementTree as ET
import urllib.request
import time
import os
import re

# clean those html tags in order to get the abstract text
def removeTag(filename):
    temp = readFile(filename)
    temp = temp.replace('<i>', '').replace('</i>', '')
    createfile(filename, temp)
    
# To create an url to use the NCBI API
def createURL(functionID, termORmids, db, numOfresults):
    entrezURL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    function = ["esearch.fcgi?db=", "efetch.fcgi?db="]      # 0:Search for MIDs, 1:Fetch for Articles
    function2 = ["&term=", "&id="]
    urlType = '&rettype=xml'
    max = '&retmax=' + str(numOfresults)  # max number of id you want, max number is between 440 - 445 because of the sine of the url
    start = '&retstart=0'
    url = entrezURL + function[functionID] + db + function2[functionID] + termORmids + urlType + start + max
    return url

# To get the xml from db
def getXML(url, filename):
    data = urllib.request.urlopen(url).read()
    createfileb(filename, data)
    removeTag(filename)
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

# To get the MIDs
def esearch(keyword, db, numOfresults):
    keyword = keyword.replace(' ', '+')
    url = createURL(0, keyword, db, numOfresults)
    root = getXML(url, './temp/dataId.xml')
    mids = []
    for id in root.find('IdList').findall('Id'):
        mids.append(id.text)
    return mids

# To get articles data
def efetch(keyword, db, numOfresults):
    mids = esearch(keyword, db, numOfresults)
    ids = ''
    counter = 0
    for index, id in enumerate(mids):
        ids += id
        if (index+1)%400 == 0 or (index+1) == len(mids): # To search for the literature's data each 400 ids
            url = createURL(1, ids, db, numOfresults)
            root = getXML(url, './temp/data.xml')
            json = gd.getdata('./temp/data.xml')
            ids = ''                                     # clear it up for next 400 ids
            json_name = './data/' + keyword + str(counter) + '.json'
            createfile(json_name,'{{{}}}'.format(','.join(json)))
            counter += 1
            time.sleep(2)
        if index != len(mids)-1 and ids != '':
            ids += ','