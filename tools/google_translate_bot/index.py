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

data = pd.read_csv("train.csv")  # import train.csv
category = data.Category.unique() #58 different categories
title = data.title

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
dir_path = os.path.dirname(os.path.realpath(__file__))
chromedriver = dir_path + '/chromedriver'
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)
driver.get("http://www.google.com/translate")
element= driver.find_element_by_xpath('//*[@id="source"]')

result = []
for i in range(0, len(title)):
    new_title = title[i]
    element.clear()
    element.send_keys(new_title)
    time.sleep(1)
    text_field = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]')
    nice_nice_text = text_field.text.split(' ')[0].lower()
    result.append(nice_nice_text)
    time.sleep(1)

data['lang'] = pd.Series(result)

data.to_csv('data_lang.csv')



