import re
import numpy as np
import pandas as pd
from pprint import pprint
import time
import sys
import os
from fileRW import createfile
from selectDB import getResult_select

import nltk; nltk.download('stopwords')
from nltk.tokenize import sent_tokenize, word_tokenize

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models import HdpModel
import gensim.downloader as api

# spacy for lemmatization
import spacy
spacy.load('en_core_web_sm')

# NLTK Stop words
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use','therefore'])
# stop_words.extend(['from', 'subject', 're', 'edu', 'use','for','the','on','in','of'])

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

def cleanup(data):
    data = [re.sub("[^a-zA-Z]", '', str(sent)) for sent in data]
    # Remove Emails
    data = [re.sub('\S*@\S*\s?', '', str(sent)) for sent in data]
    # Remove new line characters
    data = [re.sub('\s+', ' ', str(sent)) for sent in data]
    # Remove distracting single quotes
    data = [re.sub("\'", "", str(sent)) for sent in data]

def buildModel_dataset(data_words):
    start_time = time.time()
    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
    # trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    print ('Running Time for building model: ', (time.time() - start_time), 'seconds')
    return bigram_mod

# Define functions for stopwords, bigrams, trigrams and lemmatization
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(bigram_mod, texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(bigram_mod, trigram_mod, texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(nlp, texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

def preprossing(bigram_mod, data_words):
    print('Data preprossing..............')
    start_time = time.time()
    # Remove Stop Words
    data_words_nostops = remove_stopwords(data_words)
    # Form Bigrams
    data_words_bigrams = make_bigrams(bigram_mod, data_words_nostops)
    # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
    nlp = spacy.load('en', disable=['parser', 'ner'])
    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = lemmatization(nlp, data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    print ('Running Time for preprossing dataset: ', (time.time() - start_time), 'seconds')
    return data_lemmatized

def generateCorpus(data_lemmatized):
    start_time = time.time()
    # Create Dictionary
    id2word = corpora.Dictionary(data_lemmatized)
    # Create Corpus
    texts = data_lemmatized
    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]
    print ('Running Time for generating corpus: ', (time.time() - start_time), 'seconds')
    return corpus

# Saving result as txt file
def createTopfile(top_info_lda):
    start_time = time.time()
    results = []
    top_info = ''
    for top in top_info_lda:
        top_info += str(top[0]) + '\n'
        top_info += top[1]+'\n'
        words = top[1].split(' + ')
        result = []
        for word in words:
            top_word = word.split('*')
            result.append(top_word[1].replace('"', ''))
        results.append(','.join(result))
    createfile('./topicmodeling/topics.txt', '\n'.join(results))
    createfile('./topicmodeling/top_info.txt', top_info)
    print ('Running Time for creating topic result file: ', (time.time() - start_time), 'seconds')

# getting data by search pmid from DB
def loadData(pmids, numDoc):
    start_time = time.time()
    data_words = []
    if pmids:
        for index, pmid in enumerate(pmids):
            if index >= numDoc:
                break
            myresult = getResult_select('title, abstract', 'literatures', 'pmid', pmid[0])
            for result in myresult[0]:
                data_sent = list(sent_tokenize(result))
                cleanup(data_sent)
                data_words += list(sent_to_words(data_sent))
        print ('Running Time for setting up dataset: ', (time.time() - start_time), 'seconds')
        return data_words
    else:
        return []

# Start runing topic modeling
def run(num_topics, num_top_words, numDoc, pmids):
    total_start_time = time.time()
    data_words = loadData(pmids, numDoc)
    if data_words:
        bigram_mod = buildModel_dataset(data_words)
        data_lemmatized = preprossing(bigram_mod, data_words)

        start_time = time.time()
        # Create Dictionary
        id2word = corpora.Dictionary(data_lemmatized)
        # Create Corpus
        texts = data_lemmatized
        # Term Document Frequency
        corpus = [id2word.doc2bow(text) for text in texts]
        print ('Running Time for generating corpus: ', (time.time() - start_time), 'seconds')

        start_time = time.time()
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=num_topics, 
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha='auto',
                                                per_word_topics=True)
        print ('Running Time for topic modeling: ', (time.time() - start_time), 'seconds')
        top_info_lda = lda_model.print_topics(num_topics=num_topics, num_words=num_top_words)
        createTopfile(top_info_lda)
    print ('Total Running Time: ', (time.time() - total_start_time), 'seconds')