import requests
import pymysql
from bs4 import BeautifulSoup
import csv
from urllib.request import Request, urlopen

#connect to db
password = input("Enter Password: ")
conn = pymysql.connect(host = 'localhost', user='root', passwd=password,db='mysql')
cur = conn.cursor()
cur.execute("USE aquarium")

#set up beautiful soup for web scraping
site ='https://dwazoo.com/exhibit/aquarium/'
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, 'html.parser') 

#get elements with value class = entry-title
fish = soup.find_all(class_="entry-title")

#loop through fish and insert data into table
for f in fish:
    val = f.get_text().split(", ")
    query = "INSERT INTO fish (name, genus, species) VALUES ('" + val[0] + "', '" + val[1].split(' ',1)[0] + "', '" + val[1].split(' ',1)[1] + "');"
    print(query)
    cur.execute(query)
    conn.commit()

cur.close()
conn.close()

