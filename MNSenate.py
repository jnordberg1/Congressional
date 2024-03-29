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
na = "Email Not Available"
out_csv = r'C:\USS\United States Solar Corporation\Site Selection - Documents\Data\State\MN\Source\shp_bdry_senatedistricts2012\SenateMembers1.csv'

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
        print district
        districtList.append(district)
        name = rep4[0]
        nameList.append(name)
        if "(" not in rep3[2]:
            rep5 = rep3[2]
        else:
            rep5 = rep3[3]
        office = rep5
        officeList.append(office)
        
        if "St." in rep3[4]:
            rep6 = rep3[4].strip()   
        else:
            rep6 = rep3[5].strip()
        city = rep6
        cityList.append(city)
        
        if "651" in rep3[6]:
            rep7 = rep3[6]
        else:
            rep7 = rep3[7]
        phone = rep7
        phoneList.append(phone)

        if "@" in rep3[8]:
            rep8 = rep3[8]
        else:
            rep8 = na
        email = rep8
        emailList.append(email)

    driver.close()
    #pandas

    df = pd.DataFrame(np.column_stack([nameList, districtList, partyList, officeList, cityList, phoneList, emailList]),
                         columns=['Senator', 'District', 'Party', 'Office_Address', 'City_State_Zip', 'Phone_Number', 'Email'])
    df.drop_duplicates(inplace = True)
    df['Senator'] = df['Senator'].str.strip()
    df['City_State_Zip'] = df['City_State_Zip'].str.strip()
    df['Phone_Number'] = df['Phone_Number'].str.strip()
    df['District'] = df['District'].str.strip()
    df.to_csv(out_csv, index = False)

def Main():
    scrapeSenate()
    
Main()