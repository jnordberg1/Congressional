# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:16:54 2019

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

def scrapeSenate():
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
    driver.get('https://www.senate.mn/members/index.php')
    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')
    reps = soup.find_all('div', attrs={'class':'media-body align-self-center'})
    for rep in reps:
        rep1 = rep.get_text()
        rep2 = rep1.split('<b>')
        rep3 = rep2[0].split('\n')
        if "(" in rep3[1]:
            rep4 = rep3[1].split('(')
        else:
            rep4 = rep3[2].split('(')
        party = rep4[1].split(',')[1].replace(")","").replace(" ","")
        partyList.append(party)
        district = rep4[1].split(',')[0]
        districtList.append(district)
        name = rep4[0]
        nameList.append(name)
        #print rep3[2]
        if "(" in rep3[2]:
            rep5 = rep[3]
        else:
            rep5 = rep3[2]
        office = rep5
        print office
        """
        officeList.append(office)
        city = rep3[4]
        cityList.append(city)
        phone = rep3[6]
        phoneList.append(phone)
        email = rep3[8]
        emailList.append(email)
    driver.close()

    #pandas
    df = pd.DataFrame(np.column_stack([nameList, districtList, partyList, officeList, cityList, phoneList, emailList]),
                         columns=['Senator', 'District', 'Party', 'Office Address', 'City, State, Zip', 'Phone Number', 'Email'])
    df.drop_duplicates(inplace = True)
    df['Senator'] = df['Senator'].str.strip()
    df['City, State, Zip'] = df['City, State, Zip'].str.strip()
    df['Phone Number'] = df['Phone Number'].str.strip()
    df.to_csv("SenateMembers.csv", index = False)
"""
def Main():
    scrapeSenate()
    
Main()