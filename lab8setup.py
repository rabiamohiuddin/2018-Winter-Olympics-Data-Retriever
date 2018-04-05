# Lab 8: Data Storage
# Rabia Mohiuddin
# CIS 41B
# Winter 2018

import json
import sqlite3
import requests
from bs4 import BeautifulSoup 
from collections import defaultdict
import urllib.parse
import time

def retrieve(url):
    ''' Creates and returns a BeautifulSoup object using recieved url by loading the page through a Request object '''
    try:        
        page = requests.get(url)
        page.raise_for_status()    # ask Requests to raise any exception it finds      
        soup = BeautifulSoup(page.content, "lxml")  
        return soup             # Return BeautifulSoup object
    
    except requests.exceptions.HTTPError as e:         
        print ("HTTP Error:", e) 
    except requests.exceptions.ConnectionError as e:         
        print ("Error Connecting:", e) 
    except requests.exceptions.Timeout as e:         
        print ("Timeout Error:", e) 
    except requests.exceptions.RequestException as e:     # any Requests error       
        print ("Request exception: ", e)
        
def getCountryData(cSoup):
    ''' Returns a built table using a list of tuples by parsing through the recieved BeautifulSoup object '''
    table = [tuple(x for x in rows.get_text().split() if x != '') for rows in cSoup.find('div', class_= 'panel-default col-sm-6').find_all('tr')]       
    # Find the first of the two tables in div#panel-default col-sm-6 which is the Participant table, split rows by whitespace and append tuple to list (table)
    return table

def createDatabase(cur):
    cur.execute("DROP TABLE IF EXISTS Countries")      
    cur.execute('''CREATE TABLE Countries(             
                   name TEXT NOT NULL PRIMARY KEY,
                   numAthletes INT,
                   sport1 INT, sport2 INT, sport3 INT, sport4 INT, sport5 INT, sport6 INT, sport7 INT, sport8 INT, sport9 INT,
                    sport10 INT, sport11 INT, sport12 INT, sport13 INT, sport14 INT, sport15 INT)''')  
    cur.execute("DROP TABLE IF EXISTS Sports")      
    cur.execute('''CREATE TABLE Sports(             
                   id INTEGER NOT NULL PRIMARY KEY,
                   name TEXT UNIQUE ON CONFLICT IGNORE)''') 


def buildDatabase(cur, olympicSite, countryList, linkDict):
    for country in countryList:
        countrySoup = retrieve(urllib.parse.urljoin(olympicSite, linkDict[country]))  # Get soup for country's data site
        table = getCountryData(countrySoup)         # Parse site and turn it into table    
        countrySports = [None] * 15
        for num, (*name, F, M, T) in enumerate(table[1:-1]):          # List of tuples
            sportName = " ".join(name)
            cur.execute('''INSERT INTO Sports (name) VALUES (?)''', (sportName, ))
            cur.execute('SELECT id FROM Sports WHERE name = ? ', (sportName, ))        # didnt specify id, so gives it 1. Fetches id
            sport_id = cur.fetchone()[0]    
            countrySports[num] = sport_id
        
        cur.execute('''INSERT INTO Countries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (country, table[-1][-1], *tuple(countrySports)))
        time.sleep(1)           # sleep for 1 second in between getting country data
      
    
def main():
    olympicSite = "https://www.olympic.org/pyeongchang-2018/results/en/general/nocs-list.htm"
    site = retrieve(olympicSite)        # Get soup for olympic site with all participating countries
  
    countryList = [x.get_text().strip('\n') for x in site.find_all('div', class_= 'CountriesListItem')]     # list of countries
    letterDict = defaultdict(list)      # dictionary of lists
    for country in sorted(countryList):
        letterDict[country[0]].append(country)          # append each country depending on start letter
        
    with open('letterToCountryData.json', 'w') as fh:
        json.dump(letterDict, fh, indent=3)    # show indent    
    
    countryLinks = [x.get('href') for x in site.find_all('a', class_= ' center-block')]     # list of links for each country
    linkDict = dict(zip(countryList, countryLinks))     # create a dictionary by ziping country list and country links     
    
    conn = sqlite3.connect('olympics.db')
    cur = conn.cursor()     
    
    createDatabase(cur)
    buildDatabase(cur, olympicSite, countryList, linkDict)
    print("Database built")
    
    conn.commit()    
    conn.close()
    
    
main()