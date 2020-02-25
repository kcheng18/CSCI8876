from fileRW import readFile, createfile
from lxml import etree

def readXML(fileName):
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(fileName, parser=parser)
    root = tree.getroot()
    return root

def getauthors(authorsList):
    authors = []
    for author in authorsList:
        fname = author.find('ForeName').text
        lname = author.find('LastName').text
        authors.append('{{"name":"{}"}}'.format(' '.join([fname,lname])))
    return authors

def getkeywords(keywordsList):
    keywords = []
    for keyword in keywordsList:
        temp = '{{"word":"{}"}}'.format(keyword.text)
        keywords.append(temp)
    return keywords

def getdata(xmlname):
    root = readXML(xmlname)
    article_format = '"article{}":{{"pmid":"{}","title":"{}","abs":"{}","authors":[{}],"keywords":[{}]}}'
    json_list = []
    for index, article in enumerate(root.findall('PubmedArticle')):
        title = article.find('./MedlineCitation/Article/ArticleTitle').text
        abstract = article.find('./MedlineCitation/Article/Abstract/AbstractText').text
        pmid = article.find('./MedlineCitation/PMID').text
        authors = getauthors(article.findall('./MedlineCitation/Article/AuthorList/Author'))
        keywords = getkeywords(article.findall('./MedlineCitation/KeywordList/Keyword'))
        json = article_format.format(str(index),pmid,title,abstract,','.join(authors),','.join(keywords))
        json_list.append(json.replace('\n',''))
    return json_list