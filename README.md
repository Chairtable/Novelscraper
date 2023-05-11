# Novelscraper
The Novelscraper project Scrapes Novels from website to SQL Database using scraper.py and hosts Novel Chapters via Django dynamically via templates.
## Instructions
* Edit settings details in scraper.py and change URL to supported host <br>
* Currently Supports scraping of Novelhall.com specifically, other sites will need specific elements to be identified and added to be scraped
* Initialize DB Settings and Run script to scrape to SQL Server
* If Needed: Reset DB and rescrape to have novel_ID start from 1 again
* After Scraping, with django installed run 'manage.py runserver'  in the working directory to host novels from db in a readable format

## ----------TO-DO----------
* 1 Split script into separate dbsetup and scrape scripts <br>
* 2 Add novel name search function to site <br>
* 3 Santize scraped input via Base64 text. Before displaying, run it through htmlspecialchars, to keep html from working using htmlspecialchars <br>
* 4 HTML/CSS/JS styling and dynamic UI <br>

## SQL Tables:
* Table Novels (name, novelID(Primary Key), url, num_chapters)<br>
* Table Novel Chapters (novelID, chapterNum, chapterText) 
