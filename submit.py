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
import dropbox
import sys

# Get your app key and secret from the Dropbox Developer website
app_key = 'o20s8byok5kp5rg'
app_secret = 'm6dmgx3yiyftxh8'

base_url ='http://www.tinxsys.com/TinxsysInternetWeb/dealerControllerServlet?'
end_url = '&searchBy=TIN&backPage=searchByTin_Inter.jsp'


def check_tin():
    tin_no = input('Enter the tin number ')

    driver = webdriver.Chrome()
    driver.get(base_url+'tinNumber=%s'%(tin_no)+end_url)

    response = driver.page_source
    soup = BeautifulSoup(response,'html.parser')

    capture_text = soup.find_all('table')[-1]


    with open('write.txt','w') as file:
        if capture_text.find('td').text.strip() == 'Dealer Not Found for the entered TIN  %s'%(tin_no):
            print('You have entered invalid tin number\n')
        else:
            table_row_data = capture_text.find_all('tr')
            for entity in table_row_data:
                table_data = entity.find_all('td')
                write_entity = '';
                if int(len(table_data)) == 1:
                    table_data_div = table_data[0].find('div')
                    ini = table_data_div.text.replace('\n','').split(' ')
                    global title_of_file
                    title_of_file  = ini[int(ini.index('Time:'))+2]+' '+ini[int(ini.index('Time:'))+3]
                    for items in ini:
                        if items != '':
                            write_entity += (items + ' ')
                    write_entity += '\n'
                else:
                    for i in range(0,2):
                        table_data_div = table_data[i].find('div')
                        if table_data_div:
                            ini = table_data_div.text.replace('\n','').split(' ')
                        else:
                            ini = table_data[i].text.replace('\n','').split(' ')
                        for items in ini:
                            if items != '':
                                write_entity += (items + ' ')
                        if i==0:
                            write_entity += ': '
                        else:
                            write_entity += '\n'
                file.write(write_entity)



check_tin()
try:
    title_of_file
except:
    sys.exit()
# rename file with the time stamp
for filename in os.listdir("."):
    if filename.startswith("write"):
        os.rename(filename,title_of_file+'.txt')

# Have the user sign in and authorize this token
flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
authorize_url = flow.start()

driver = webdriver.Chrome()
driver.get(authorize_url)
print('User please authorise yourself within 100 seconds :)')

WebDriverWait(driver,100).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "auth-button"))
)
print('User logged in!!')
allow_user = driver.find_element_by_xpath("//button[@class='auth-button button-primary']")
allow_user.click()

WebDriverWait(driver,10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "auth-connect-frame"))
)
print('please have patience , sit and relax :)')
response = driver.page_source
soup = BeautifulSoup(response,'html.parser')

final_call = soup.find('input',{'class','auth-box'})
code = final_call.get('data-token').strip()

# This will fail if the user enters an invalid authorization code
access_token, user_id = flow.finish(code)
client = dropbox.client.DropboxClient(access_token)

f = open(title_of_file + '.txt', 'rb')
response = client.put_file('/'+title_of_file + '.txt', f)
print("UPLOAD SUCCEEDED , LOOK INTO DROPBOX :)")
driver.quit()
