from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import numpy as np
import pandas as pd
import csv
import time

stoppedwhere=2

def get_list_all_files_name(dir_path):
    all_files_path = []

    for (dirpath, dirnames, filenames) in os.walk(dir_path):
        for f in filenames:
            all_files_path.append(os.path.join(dirpath, f))

    return all_files_path

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
dir_path = os.path.dirname(os.path.realpath(__file__))
chromedriver = dir_path + '/chromedriver'
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)
driver.get("http://www.google.com/translate")
element= driver.find_element_by_xpath('//*[@id="source"]')



listoffiles=get_list_all_files_name('flatter_splitted_data/')

# restructure listoffiles into ascending order
keys = []
file_map = {}
for i in range(0, len(listoffiles)):
    singlefile = listoffiles[i]
    singlefilename = int(singlefile.split('/')[1].split('.')[0])
    keys.append(singlefilename)
    file_map[singlefilename] = singlefile

listoffiles=[]
for i in range(stoppedwhere, len(keys)+stoppedwhere):
    listoffiles.append(file_map[i])


# start crawling for data
for i in range(0, len(listoffiles)):
    lang_result = []
    transtext_result = []
    singlefile = listoffiles[i]
    singlefilename = singlefile.split('/')[1].split('.')[0]
    print('currently processing : ', singlefilename )
    data = pd.read_csv(singlefile) 
    title = data.title
    start = time. time()
    for j in range(0, len(title)):
        new_title = title[j]
        element.clear()
        element.send_keys(new_title)
        time.sleep(1)
        try:
            lang_text_field = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]')
            lang = lang_text_field.text.split(' ')[0].lower()
            lang_result.append(lang)
        except:
            time.sleep(1)
            lang_text_field = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]')
            lang = lang_text_field.text.split(' ')[0].lower()
            lang_result.append(lang)

        if lang=='english':
            transtext_result.append(new_title)
        else :
            time.sleep(1)
            try:
                trans_text_field = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div/span[1]')
                trans_text = trans_text_field.text.lower()
                transtext_result.append(trans_text)
            except:
                time.sleep(1)
                trans_text_field = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div/span[1]')
                trans_text = trans_text_field.text.lower()
                transtext_result.append(trans_text)

        if j%100==0:
            print(j)


    end = time. time()
    print(end - start)


    data['language'] = pd.Series(lang_result)
    data['english'] = pd.Series(transtext_result)

    os.remove(singlefile)
    print("File Removed!")

    time.sleep(3)

    data.to_csv('./extended_data/'+singlefilename+'.csv',mode = 'w', index=False)
    print('write to ' +singlefilename )
    time.sleep(3)








# --- split file to 1000 lines/file
# split -l 1000 train.csv
# for i in *; do mv "$i" "$i.csv";

# --- change name of file
# a=1
# for i in *; do
#   new=$(printf "%03d.csv" "$a") #04 pad to length of 4
#   mv -i -- "$i" "$new"
#   let a=a+1
# done

# --- add header to all .csv file in folder
# --- https://stackoverflow.com/questions/33787264/adding-header-to-all-csv-files-in-folder-and-include-filename
# for i in *.csv;do echo $i;cp "$i" "$i.bak" && { echo "itemid,title,Category,image_path"; cat "$i.bak"; } >"$i";done

# -- remove all .bak file in folder
# rm *.bak

# -- need remove 001.csv extra header

