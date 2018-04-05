# Data Storage
# Rabia Mohiuddin
# Winter 2018

import sqlite3
import json

def displayOptions():
    ''' Display 3 options to user and return selected number corresponding to choice '''
    print("Enter the number corresponding to the option of your choice or the number 0 at the prompt to quit\n")
    print("[1] Display number of athletes for one country")
    print("[2] Display all countries that participated in one sport")
    print("[3] Display countries with certain number of athletes\n")
    
    strChoice = input("Option number: ")
    while strChoice != "0":
        try:
            intChoice = int(strChoice)
            if 0 <= intChoice <= 3: return intChoice        # If between [1, 3]: return
            else: raise ValueError
        
        except ValueError:
            print("Input must be a number and one of the options above - between 1 and 3")
            strChoice = input("\nOption number: ")        
    
    return 0      # return 0 to indicate quit

def ch1countryAthletes(cur):
    ''' [1] Display number of athletes for one country '''
    with open('letterToCountryData.json', 'r') as fh:
        countryLetterDict = json.load(fh)
        
    firstLtr = input("First letter of country name: ").upper()
    while firstLtr not in countryLetterDict:          # Keep prompting until valid input
        if firstLtr.isalpha(): print("No countries that start with letter", firstLtr)   # If letter exists in dictionary
        elif firstLtr =='0': return             # If user wants to quit
        else: print("Input must be a letter")       # If anything besides a letter
        firstLtr = input("\nFirst letter of country name: ").upper()
        
    print("Countries participating in the Winter Olympics:")
    for i, country in enumerate(countryLetterDict[firstLtr], start=1):    # Print countries starting with entered letter
        print(i, '-' , country)     
    
    strChoice = input("Pick a number corresponding to the country: ")
    while strChoice != "0":
        try:
            numChoice = int(strChoice)          # Convert to int
            if 0 < numChoice <= len(countryLetterDict[firstLtr]): break      # If number is one of the choices, break and continue
            else: raise ValueError          # If anything else, raise exception
                
        except ValueError as v:
            print("\nInput must be a number and one of the options above - between 1 and", len(countryLetterDict[firstLtr]))
            strChoice = input("Pick a number corresponding to the country: ")   
    
    country = countryLetterDict[firstLtr][numChoice-1]
    cur.execute("SELECT numAthletes FROM Countries WHERE name = ?", (country,))
    print(cur.fetchone()[0], "athletes for", country)
    
        
def ch2sportCountries(cur):
    ''' [2] Display all countries that participated in one sport '''
    print("Sports:")
    sportsList = [name[0] for name in cur.execute("SELECT name FROM Sports")]
    print(", ".join(sportsList))
    
    sportName = input("Enter sport name: ").title()
    while sportName not in sportsList:
        print("Sport does not exist")
        sportName = input("\nEnter sport name: ").title()

    print("\nCountries participating in", sportName)
    cur.execute("Select id FROM Sports WHERE name = ?", (sportName,))
    sportId = cur.fetchone()[0]
    
    cur.execute("SELECT Countries.name FROM Countries JOIN Sports ON Countries.sport1 = Sports.id OR Countries.sport2 = Sports.id OR Countries.sport4 = Sports.id OR Countries.sport5 = Sports.id OR Countries.sport6 = Sports.id OR Countries.sport7 = Sports.id OR Countries.sport8 = Sports.id OR Countries.sport9 = Sports.id OR Countries.sport10 = Sports.id OR Countries.sport11  = Sports.id OR Countries.sport12 = Sports.id OR Countries.sport13 = Sports.id OR Countries.sport14 = Sports.id OR Countries.sport15 = Sports.id WHERE Sports.id = ?", (sportId,))
    
    for country in cur.fetchall(): print(country[0])
    
    
def ch3certainAthletes(cur):
    ''' [3] Display countries with certain number of athletes '''
    notCorrect = True
    while notCorrect:
        strRange = input("Enter min, max number of athletes: ")
        try:
            if len(strRange.split(', ')) != 2: raise ValueError("Must only enter two numbers in format min, max")
            
            small = int(strRange.split(', ')[0])        
            big = int(strRange.split(', ')[1])
            
            if small > big: raise ValueError("Min is greater than max. Please input a valid range")
            
            notCorrect = False
        except ValueError as v:
            print(v)
            strRange = input("\nEnter min, max number of athletes: ")
    
    print("Countries with", small, "to", big, "athletes")
    cur.execute("Select name FROM Countries WHERE numAthletes BETWEEN ? AND ? ORDER BY name ASC", (small, big))
    
    countryList = [country[0] for country in cur.fetchall()]
    # print countries
    if len(countryList) == 0: print("No countries with athletes in range", small, "to", big)
    for country in countryList: print(country)
    

def main():
    print("Welcome to the PyeongChang 2018 Olympic Winter Games Data Retriever!")
    choice = displayOptions()           # display options to the user
    
    conn = sqlite3.connect('olympics.db')
    cur = conn.cursor()   
    
    while choice != 0:
        if choice == 1: ch1countryAthletes(cur)     # pass the cursor to choice 1
        elif choice == 2: ch2sportCountries(cur)    # pass the cursor to choice 2
        elif choice == 3: ch3certainAthletes(cur)    # pass the cursor to choice 3
        print()
        choice = displayOptions()
        
    conn.close()    
              
main()
