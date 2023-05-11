from operator import truediv
from selenium import webdriver
from selenium.webdriver.common.by import By
import mysql.connector
import time
# Novelscraper project Scrape Script
# Edit settings details below and change URL to supported host
# Currently Supports scraping of Novelhall.com specifically, other sites will need specific elements to be identified and added to be scraped
# Initialize DB Settings and Run script to scrape to SQL Server
# If Needed: Reset DB and rescrape to have novel_ID start from 1 again
# After Scraping, with django installed run 'manage.py runserver'  in the working directory to host novels from db in a readable format

# #------------TO-DO----------
# 1 Split script into separate dbsetup and scrape scripts
# 2 Add novel name search function to site 
# 3 Santize scraped input via Base64 text. Before displaying, run it through htmlspecialchars, to keep html from working using htmlspecialchars
# 4 HTML/CSS/JS styling and dynamic UI 

# # SQL Tables:
# # Table Novels (name, novelID(Primary Key), url, num_chapters)
# # Table Novel Chapters (novelID, chapterNum, chapterText) 


##Enter your SQL Server Details Below:
#SQL Server
mydb = mysql.connector.connect(
host="localhost",
user="root",         ###Your Username here
password="",         ###Your Password Here
database = 'novels', ###Your DB Here, use novels for less code to be changed
autocommit=True)

mycursor = mydb.cursor(buffered=True)

#Initial setup to create the novelslist and novelChapters tables in the novels database
def dbSetup():
    mycursor.execute("""CREATE DATABASE IF NOT EXISTS novels""")
    mycursor.execute("""USE novels""")          ###Your DB here (as above in SQL Server Details)
    #Make novelslist table
    mycursor.execute("""Create TABLE IF NOT EXISTS novelslist(
        Novel_Name VARCHAR(200) NOT NULL, 
        Novel_ID INT NOT NULL AUTO_INCREMENT, 
        Novel_URL VARCHAR(200) NOT NULL, 
        Novel_Numchapters INT,
        PRIMARY KEY (Novel_ID))""")
    #Make novelchapters table
    mycursor.execute("""Create TABLE IF NOT EXISTS novelChapters(
        Chapter_ID INT NOT NULL AUTO_INCREMENT,
        Novel_ID INT, 
        Chapter_Num INT, 
        Chapter_Text TEXT,
        PRIMARY KEY (Chapter_ID),
        FOREIGN KEY (Novel_ID) REFERENCES novelslist(Novel_ID))""")

#Check if the novel exists in the novelslist table, returns true if the name is found, false if it is not
def checkNovelExists(novelName):
    query = "Select '{}' from novelslist".format(novelName)
    mycursor.execute(query)
    result = mycursor.fetchall()
    print("Result is", result)
    for row in result:
        print("Name: " + novelName)
        if novelName == row[0]:
            print("Novel in database")
            return True
    print("Novel not in database)")
    return False

#Adds the novel info to the novelslist table in the database
def addNovelToDB(novelUrl):
    novelTitle = getNovelTitle(novelUrl)
    numChaps = getNumChapters(novelUrl)
    if checkNovelExists(novelTitle) == False:
        print("Adding novel info to database")
        query = "Insert Into novelslist (Novel_Name, Novel_URL, Novel_Numchapters) VALUES ('{}', '{}', {})".format(novelTitle, novelUrl, numChaps)
        mycursor.execute(query)

#Returns the ID of the novel, assuming it exists in the novelslist table of the database
def getNovelID(novelTitle):
    query = "Select Novel_ID from novelslist where novel_name = '{}'".format(novelTitle)
    mycursor.execute(query)
    result = mycursor.fetchone()
    return result[0]

def htmlspecialchars(text):
    return (
        text.replace("&", "&amp;").
        replace('"', "&quot;").
        replace("<", "&lt;").
        replace(">", "&gt;")
    )

#Chrome webdriver
options = webdriver.ChromeOptions() 
options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe"  ###Enter your chrome.exe location here
#options.setBinary("C:\Program Files\Google\Chrome Beta\Application\chrome.exe");
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options, executable_path='C:\Program Files\Google\Chrome Beta\chromedriver\chromedriver.exe')###Enter your chromedriver.exe path here
baseUrl = 'https://www.novelhall.com/Since-The-Red-Moon-Appeared-18566/' ###Enter your novelhall URL 
driver.get(baseUrl)

#Get the number of chapters by checking list length for chapters in the NovelHall URL 
def getNumChapters(novelUrl):
    numChapters = 0
    driver.get(novelUrl) 
    chapterListElement = driver.find_element(By.XPATH, '//*[@id="morelist"]/ul') #//*[@id="main"]/div/div[2]/ul/li[10] may have to be clicked if errors
    chapterListItem = chapterListElement.find_elements_by_tag_name("li")
    for li in chapterListItem:
        numChapters+=1
    return numChapters

#Retunrs the title of the novel
def getNovelTitle(novelUrl):
    driver.get(novelUrl)
    novelTitle = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/div[2]/h1').text
    return novelTitle

#Returns the number of chapters the novel has in the database
def getNovelDBChapterStatus(novelID):
    query = 'Select COUNT(*) FROM novelchapters where Novel_ID = {}'.format(novelID)
    mycursor.execute(query)
    result = mycursor.fetchone()
    return result[0]

#Returns the text of the chapter from the chapter page
def getChapterText(chapterLink):
    driver.get(chapterLink)        
    textElement = driver.find_element(By.XPATH, '//*[@id="htmlContent"]').text
    return textElement

def getAllChapters(novelUrl):
    numChapters = getNumChapters(novelUrl)
    novelTitle = getNovelTitle(novelUrl)
    if checkNovelExists(novelTitle) == True:
        novelID = getNovelID(novelTitle)
        numDBChapters = getNovelDBChapterStatus(novelID)
        for i in range (numDBChapters+1, numChapters+1):
            chapterXPATH = '//*[@id="morelist"]/ul/li[{}]/a'.format(i)
            chapterLink = driver.find_element(By.XPATH, chapterXPATH).get_attribute('href')
            chapterText = getChapterText(chapterLink)
            query = "Insert Into novelChapters VALUES (default, {}, {}, '{}')".format(novelID, i, chapterText) 
            mycursor.execute(query)
            print("Scraped Chapter: " + str(i) + " of " + str(numChapters))
            time.sleep(1.5)  ##Sleep to prevent getting stuck and/or scrape protection
            driver.get(novelUrl)
    else: #If the novel does not exist in the database then add to DB and scrape from chapter 1 onwards
        addNovelToDB(novelUrl)
        novelID = getNovelID(novelTitle)
        for i in range (1, numChapters+1):
            chapterXPATH = '//*[@id="morelist"]/ul/li[{}]/a'.format(i)
            chapterLink = driver.find_element(By.XPATH, chapterXPATH).get_attribute('href')
            chapterText = getChapterText(chapterLink)
            query = "Insert Into novelchapters (Novel_ID, Chapter_Num, Chapter_Text) VALUES ({}, {}, '{}')".format(novelID, i, chapterText)
            mycursor.execute(query)
            print("Scraped Chapter: " + str(i) + " of " + str(numChapters))
            time.sleep(1.5)
            driver.get(novelUrl)
dbSetup()
getAllChapters(baseUrl)
print("Completed Scrape")
driver.close()

