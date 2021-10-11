from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from sqlalchemy import  create_engine



full_website = 'http://books.toscrape.com/catalogue/page-40.html'
urlz = 'http://books.toscrape.com/catalogue/page-'
newbook_list = []
for page in range(1,51):
    r = requests.get(urlz + str(page) + '.html')
    souper = BeautifulSoup(r.text, 'html.parser')
    boz = souper.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

    for bo in boz:
        full_namez = bo.find('h3').contents[-1]['title'].strip()
        pricez = bo.find('div', class_='product_price')('p')[0].text.replace('Â£','')
        currency = bo.find('div', class_='product_price')('p')[0].text[1]
        availablez = bo.find('div', class_='product_price')('p')[1].text.strip()
        url = 'https://www.' + bo.find('a')['href']
        bok = bo.find('div', class_='image_container')('img')
        for img in bok:
            pass
        img_link = 'http://books.toscrape.com' + img['src']

        bookz = {
        
        'Title':full_namez,
        'Currency':currency,
        'Price':pricez,
        'Availability':availablez,
        'URL':url,
        'Img_URL':img_link
        } 

        newbook_list.append(bookz)
    new_df = pd.DataFrame(newbook_list)
    #change price section to int
    new_df['Price'] = pd.to_numeric(new_df.Price)
    new_df

df = new_df
engine = create_engine('sqlite:///pdsql.db', echo=True)
sqlite_connection = engine.connect()


book_table = 'books'
df.to_sql(book_table, sqlite_connection, if_exists='fail')


