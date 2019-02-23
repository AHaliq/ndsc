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



listoffiles=get_list_all_files_name('splitted_data/')

for i in range(0, len(listoffiles)):

    lang_result = []
    transtext_result = []
    singlefile = listoffiles[i]
    data = pd.read_csv(singlefile)  # import train.csv
    title = data.title
    for j in range(0, len(title)):
        new_title = title[j]
        element.clear()
        element.send_keys(new_title)
        time.sleep(1.25)

        lang_text_field = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]')
        lang = lang_text_field.text.split(' ')[0].lower()
        lang_result.append(lang)

        time.sleep(1)

        trans_text_field = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/div[2]/div/span[1]')
        trans_text = trans_text_field.text
        transtext_result.append(trans_text)



    data['language'] = pd.Series(lang_result)
    data['english'] = pd.Series(transtext_result)

    time.sleep(3)

    data.to_csv('/extended_data/'+i+'.csv')
    print('write to ' + i)
    time.sleep(3)
