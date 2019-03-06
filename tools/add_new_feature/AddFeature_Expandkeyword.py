import numpy as np
import pandas as pd
import csv
import nltk
import math
import io 
from nltk.corpus import stopwords 
stoplist = set(stopwords.words("english"))

# this file is use to generate "Translate" feature for both "train" and "test" set

type_of_file = 'test' # test or train


#num of categories
CATEGORY = 58

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
    'best selling', # everythign is best selling
    'cheapest', # everything is cheapest
    'best', # everything is best
    'sale', # everything is on sale
    'official', # all mobiles are official
    'original', # everything is original
]

# append to stoplist with handpicked_stoplist
for word in handpicked_stoplist:
    stoplist.add(word)


def translate_bahasa_to_english(df):

    # tokenize the every row of title
    df['title'] = df['title'].apply(lambda x: x.split(' '))

    titles = df['title']

    # translate and drop word(s)
    for title in titles:
        for word in title:
            # translation
            if word in words_to_translate:
                title[title.index(word)] = words_to_translate[word]

        for word in title:
            if(len(title)<1):
                break
            # drop word
            if word in stoplist:
                title.remove(word)
    
    df['title'] = df['title'].apply(lambda x: ' '.join(x))
   
    
    return df
            

def write_to_file(df, file_name):
    df.to_csv(file_name,mode = 'w', index=False)



if type_of_file =='test':
    input_file = '../data/clean/test_englishfeature.csv'
    output_file = '../data/clean/test.csv'
    require_word_txt = 'Gen_ImptWords_5_flatten.txt'

    # read imptwords 
    df_input = pd.read_csv(input_file)
    imptwords = open(require_word_txt, 'r').read()

    # translate bahasha to english first
    const_df_input_translated = pd.read_csv(input_file) # input that dosent change
    df_input = translate_bahasa_to_english(df_input)
    df_input_headers = list(df_input.columns.values)
    df_input_itemid = df_input['itemid']

    
    # flatten require_word_txt and add to df as column header
    flatten_column = imptwords.split('|')
    
    # initialize new df to store the final df
    df_allfeatures = pd.DataFrame(columns= df_input_headers + flatten_column)


    # way two
    zeroes = np.zeros((len(df_input), len(flatten_column)))
    df_input['title'] = df_input['title'].apply(lambda x: x.split(' '))
    for x, title in enumerate(df_input['title'] ):
        for y, word in enumerate(title):
            if word in flatten_column:
                zeroes[x][flatten_column.index(word)] = 1

    zeroes = pd.DataFrame(zeroes, columns=flatten_column)

    # merge both original df and zeroes df
    df_allfeatures = pd.concat([const_df_input_translated, zeroes], axis=1, join_axes=[const_df_input_translated.index])


    
    write_to_file(df_allfeatures, 'test.csv')
   
elif type_of_file=='train':
    input_file = '../data/clean/train_translated_numeric.csv'
    output_file = './data/clean/train_new.csv'
    require_word_txt = 'Gen_ImptWords_5_flatten.txt'

    # read imptwords 
    df_input = pd.read_csv(input_file)
    imptwords = open(require_word_txt, 'r').read()

    # translate bahasha to english first
    const_df_input_translated = pd.read_csv(input_file) # input that dosent change
    df_input = translate_bahasa_to_english(df_input)
    df_input_headers = list(df_input.columns.values)
    df_input_itemid = df_input['itemid']

    
    # flatten require_word_txt and add to df as column header
    flatten_column = imptwords.split('|')
    
    # initialize new df to store the final df
    df_allfeatures = pd.DataFrame(columns= df_input_headers + flatten_column)


    # way two
    zeroes = np.zeros((len(df_input), len(flatten_column)))
    df_input['title'] = df_input['title'].apply(lambda x: x.split(' '))
    for x, title in enumerate(df_input['title'] ):
        for y, word in enumerate(title):
            if word in flatten_column:
                zeroes[x][flatten_column.index(word)] = 1

    zeroes = pd.DataFrame(zeroes, columns=flatten_column)

    # merge both original df and zeroes df
    df_allfeatures = pd.concat([const_df_input_translated, zeroes], axis=1, join_axes=[const_df_input_translated.index])


    
    write_to_file(df_allfeatures, 'train.csv')
