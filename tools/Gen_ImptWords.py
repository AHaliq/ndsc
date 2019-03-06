import numpy as np
import pandas as pd
import csv
import nltk
import math
import io 
from nltk.corpus import stopwords 
stoplist = set(stopwords.words("english"))


# any input file with 'Category' and 'title'
input_file = '../data/clean/train_translated_numeric.csv'

output_file = 'Gen_ImptWords_5.csv'
output_file_flatten = 'Gen_ImptWords_5_flatten.txt'

words_to_translate = {
        'untuk':'for', 
        'murah':'cheap',
        'bedak':'powder',
        'tabur':'sprinkle',
        'paket':'package',
        'wajah':'face',
        'tahan':'hold it down',
        'produk':'product',
        'terlaris':'best selling',
        'terbaru':'the latest',
        'wanita':'woman',
        'lengan':'arm',
        'pesta':'party',
        'panjang':'long',
        'baju':'clothes',
        'brokat':'brocade',
        'gaun':'dress',
        'kaos':'t-shirt',
        'pendek':'short',
        'motif':'motive',
        'bahan':'ingredients',
        'warna':'color',
        'tanpa':'without',
        'dengan':'with',
        'musim':'season',
        "ukuran":"size",
        "besar":"big",
        "atasan":"boss",
        "kemeja":"shirt",
        "longgar":"loose",
        "panas":"hot",
        "blus":"blouse",
        "garansi":"warranty",
        "resmi":"official",
        "beli":"buy",
        "hitam":"black",
        "berkualitas":"quality",
        "dijual":"on sale",
        "termurah":"cheapest",
        "perdana":"prime",
        "terbatas":"limited",
        'bergaransi':'guaranteed',
        'tahun':'year',
    }
handpicked_stoplist = [
    'new',# all shit is new 
    'promo', # all shit is under promotion
    'cheap', # everything is cheap
    'best selling', # everything is best selling
    'cheapest', # everything is cheapest
    'best', # everything is best
    'sale', # everything is on sale
    'official', # all mobiles are official
    'original', # everything is original
]

# append to stoplist with handpicked_stoplist
for word in handpicked_stoplist:
    stoplist.add(word)

#num of categories
CATEGORY = 58

#num of impt words
NUM_IMPT_WORDS = 5

def computeTF(wordDict, bow):
    tfDict = {}
    bowCount = len(bow)
    for word, count in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict

def computeIDF(list_of_docs):
    idfDict={}
    N = len(list_of_docs)

    # all the words exist in all the titles in that category 
    all_words = []
    for doc in list_of_docs:
        for word in doc:
             all_words.append(word)
        
    # make a dictionary our of all unique word from documents of that particular category
    idfDict = dict.fromkeys(set(all_words), 0)

    # count the number of doc contain the word w
    for doc in list_of_docs:
        for word in set(doc): # ensure all unique word
            idfDict[word]+=1 # plus one document 
    
    for word, val in idfDict.items():
        idfDict[word] = math.log(N/float(val))

    return idfDict

def computeTFIDF(tfBow, idfs):
    tfidf={}
    for word, val in tfBow.items():
        tfidf[word] = val * idfs[word]
    return tfidf

df = pd.read_csv(input_file)
result = [] # arr of df
flatten_result = []
for i in range(0, CATEGORY):

    # all the title in the given category, result will be [[w1,w2,w3],[wa,wb,wc,wd,we]....]
    list_of_docs = df[df['Category']==i]['title'].apply(lambda x: x.split(' ') )

    # remove stop words in list_of_docs
    for doc in list_of_docs:
        for word in doc:
            if word in words_to_translate:
                doc[doc.index(word)] = words_to_translate[word]

        for word in doc:
            if word in stoplist:
                doc.remove(word)

            
    # total number of titles
    total_docs = len(list_of_docs)

    # all the words exist in all the titles in that category 
    all_words = []
    for doc in list_of_docs:
        for word in doc:
             all_words.append(word)
        
    # make a dictionary our of all unique word from documents of that particular category
    dictionary = dict.fromkeys(set(all_words), 0)

    # count terms
    for word in all_words:
        dictionary[word]+=1

    # cal tf
    tf = computeTF(dictionary, list_of_docs)

    # cal idf
    idfs = computeIDF(list_of_docs)

    
    all_words = set(all_words)
    for word in all_words:
        dictionary[word] = tf[word] * idfs[word]
    
    temp_arr = sorted(dictionary, key=lambda x: (-dictionary[x], x))[:NUM_IMPT_WORDS]

    result.append({ 'Category': i, 'keywords':temp_arr})
    
    flatten_result += temp_arr


final = pd.DataFrame(columns = ['Category','keywords'])
final = final.append(result)

# output csv file
final.to_csv(output_file,mode = 'w', index=False)

# output txt file, list of keywords 1D
flatten_result = set(flatten_result)
flatten_result = list(flatten_result)
flatten_result =  '|'.join(flatten_result).replace('[','').replace(']', '')
mylist = dir()
with open(output_file_flatten,'w') as f:
    f.write(flatten_result)