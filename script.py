from optparse import OptionParser
import json
import re
import os,errno
import shutil
from datetime import datetime, timedelta
import time
import urllib
import requests
import operator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup

base_url = 'http://codechef.com/problems/'
#problem_name = 'CHEFPRES'

def best_sol():

    problem_name = input("Enter the problem code for codechef.com ")

    driver = webdriver.Chrome()
    driver.get(base_url+problem_name)
    print('Opening codechef.com ....')


    # click on the + button (Successful submission) to expand it
    open_submission = driver.find_element_by_xpath("//button[@class='toogle-button fa fa-plus-square-o']")
    open_submission.click()

    WebDriverWait(driver,10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "table-questions"))
    )

    response = driver.page_source
    soup = BeautifulSoup(response,'html.parser')
    #print(soup.prettify())

    # find out the best solution
    tot = (soup.find("table",{"class":"dataTable"}).find('tbody').find_all('tr'))[0].find_all('a')[1].get('href')
    final_link = 'https://www.codechef.com' + str(tot)

    driver.get(final_link)
    print("Openinf url: %s"%(final_link))

    response1 = driver.page_source
    soup1 = BeautifulSoup(response1,'html.parser')

    chk = soup1.find_all('ol')[0]


    with open("code_%s.txt"%(problem_name),'w') as file:
        print('Downloading code...')
        list_to_scan = chk.find_all('li')
        for line in list_to_scan:
            file.write(line.text+'\n')

    print('Code downloaded')

best_sol()
