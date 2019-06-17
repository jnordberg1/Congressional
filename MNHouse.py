# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 09:59:31 2019

@author: JacobNordberg
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import numpy as np
import os
script_path = r'C:\Users\JacobNordberg\Documents\GitHub\Congressional'
os.chdir(script_path)
print "Start time:"
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
nameList = []
districtList = []
partyList = []
officeList = []
cityList = []
phoneList = []
emailList = []
def scrapeHouse():
    option = webdriver.ChromeOptions()
    chrome_prefs = {}
    option.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = { "popups": 1 }
    driver = webdriver.Chrome(chrome_options=option)
    #user_agent = 'Chrome/60.0.3112.50'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('user-agent={user_agent}')
    driver = webdriver.Chrome() #requires chromedriver.exe
    driver.get('https://www.house.leg.state.mn.us/members/')
    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')
    reps = soup.find_all('div', attrs={'class':'media-body'})
    for rep in reps:
        rep1 = rep.get_text()
        rep2 = rep1.split('/b')
        rep3 = rep2[0]
        rep4 = rep3.split('\n')
        name = rep4[1].split('(')
        name1 = name[0]
        nameList.append(name1)
        party = rep4[1].split(',')[-1].replace(")","").replace(" ","")
        partyList.append(party)
        district = rep4[1].split(',')[0]
        district1 = district[-3:]
        districtList.append(district1)
        office = rep4[2].strip()
        officeList.append(office)
        city = rep4[4].strip()
        cityList.append(city)
        phone = rep4[6].strip()
        phoneList.append(phone) 
        email = rep4[8].strip()
        emailList.append(email)
    driver.close()
    #pandads
    df = pd.DataFrame(np.column_stack([nameList, districtList, partyList, officeList, cityList, phoneList, emailList]),
                         columns=['House Member', 'District', 'Party', 'Office Address', 'City', 'Phone Number', 'Email'])
    df.drop_duplicates(inplace = True)
    df['House Member'] = df['House Member'].str.strip()
    df.to_csv("HouseMembers.csv", index = False)
    
    return df        
df = scrapeHouse()