from fileRW import readFile, createfile
from lxml import etree

def checkNone(xmlobject):
    if xmlobject != None:
        return  xmlobject.text
    else:
        return ''

def readXML(fileName):
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(fileName, parser=parser)
    root = tree.getroot()
    return root

def getauthors(authorsList):
    authors = []
    for author in authorsList:
        fname = checkNone(author.find('ForeName'))
        lname = checkNone(author.find('LastName'))
        authors.append('{{"name":"{}"}}'.format(' '.join([fname,lname])))
    return authors

def getkeywords(keywordsList):
    keywords = []
    for keyword in keywordsList:
        temp = '{{"word":"{}"}}'.format(keyword.text)
        keywords.append(temp)
    return keywords

def getdate(date):
    month = checkNone(date.find('Month'))
    year = checkNone(date.find('Year'))
    day = checkNone(date.find('Day'))
    return '{}-{}-{}'.format(year,month,day)

def getdata(xmlname):
    root = readXML(xmlname)
    article_format = '"article{}":{{"pmid":"{}","title":"{}","date":"{}","abs":"{}","authors":[{}],"keywords":[{}]}}'
    json_list = []
    for index, article in enumerate(root.findall('PubmedArticle')):
        title = str(checkNone(article.find('./MedlineCitation/Article/ArticleTitle'))).replace('"', '')
        abstract = str(checkNone(article.find('./MedlineCitation/Article/Abstract/AbstractText'))).replace('"', '')
        if title != '' and abstract != '':
            pmid = checkNone(article.find('./MedlineCitation/PMID'))
            authors = getauthors(article.findall('./MedlineCitation/Article/AuthorList/Author'))
            keywords = getkeywords(article.findall('./MedlineCitation/KeywordList/Keyword'))
            date = getdate(article.find('./MedlineCitation/DateRevised'))
            json = article_format.format(str(index),pmid,title,date,abstract,','.join(authors),','.join(keywords))
            json_list.append(json.replace('\n',''))
    return json_list