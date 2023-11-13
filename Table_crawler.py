from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import json
import re

def split_date(date_string):
    match = re.match(r"(\d+)[^\d]*(\d*)[^\w]+(\w+)", date_string)

    if match:
        start_day, end_day, month = match.groups()
        if end_day:
            start_date = f"{start_day} {month}"
            end_date = f"{end_day} {month}"
            return {'start_date': start_date, 'end_date': end_date}
        else:
            single_date = f"{start_day} {month}"
            return {'start_date': single_date, 'end_date': single_date}
    else:
        return None
    
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)
url_modi = "https://en.wikipedia.org/wiki/List_of_international_prime_ministerial_trips_made_by_Narendra_Modi"
driver.get(url_modi)
time.sleep(2)

# Locators
soup = BeautifulSoup(driver.page_source, 'html.parser')
tables = soup.find_all('table', class_='wikitable outercollapse sortable jquery-tablesorter')
headlines =soup.find_all('span', class_='mw-headline')
year_list=[]
modi_dic=[]

#Extract years
for headline in headlines:
     if headline.text.strip().isdigit():
          year_list.append(headline.text.strip())

          

# Extract data from specific columns
index=0
for table in tables:
    data_list = []
    for row in table.find_all('tr'): 
        country_name = ''
        city_list = []
        date_entry = ''
        
        columns = row.find_all('td')
        if len(columns) > 1:
            if (columns[0].has_attr('rowspan') or columns[0].text.strip().isdigit()):
                    country_name = columns[1].text.strip()
                    links = columns[2].find_all('a')
                    city_list = list(set(a.text.strip() for a in links))
                    date_entry = columns[3].text.strip()
            else: 
                country_name = columns[0].text.strip()
                links = columns[1].find_all('a')
                city_list = list(set(a.text.strip() for a in links))
                date_entry = columns[2].text.strip()
            if country_name and city_list and date_entry:
                data_list.append({
                    'Country': country_name,
                    'City': city_list,
                    'Date': split_date(date_entry),
                })
    modi_dic.append({
        'Year':year_list[index],
        'Visits':data_list
    })
    index+=1

json_data = json.dumps(modi_dic, indent=2)  # indent for pretty formatting

# Save the JSON data to a file
with open('modi1.json', 'w') as json_file:
    json_file.write(json_data)