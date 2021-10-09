from bs4 import BeautifulSoup
import requests
import json
from flask import  Flask, render_template, jsonify
import pandas as pd
import numpy as np





app = Flask(__name__)


@app.route('/')
def books():
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

            bookz = {
            
            'Title':full_namez,
            'Currency':currency,
            'Price':pricez,
            'Availability':availablez,
            'URL':url
            } 

            newbook_list.append(bookz)
    new_df = pd.DataFrame(newbook_list)
    #change price section to int
    new_df['Price'] = pd.to_numeric(new_df.Price)
    new_df
    return render_template('books.html',  tables=[new_df.to_html(classes="table table-striped table-hover")], titles=new_df.columns.values)
    

@app.route('/json')
def json_format():
    full_website = 'http://books.toscrape.com/catalogue/page-40.html'
    urls = 'http://books.toscrape.com/catalogue/page-'
    newbook_list = []
    for page in range(1,51):
        r = requests.get(urls + str(page) + '.html')
        souper = BeautifulSoup(r.text, 'html.parser')
        boz = souper.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

        for bo in boz:
            full_names = bo.find('h3').contents[-1]['title'].strip()
            prices = bo.find('div', class_='product_price')('p')[0].text.replace('Â£','')
            currency = bo.find('div', class_='product_price')('p')[0].text[1]
            availables = bo.find('div', class_='product_price')('p')[1].text.strip()
            url = 'https://www.' + bo.find('a')['href']

            books = {
            
            'title':full_names,
            'currency type':currency,
            'price':prices,
            'availability':availables,
            'url':url
            }
          

            newbook_list.append(books)
        #convert values of price to float
        for i in range(0,len(newbook_list)):
            newbook_list[i]['price'] = float(newbook_list[i]['price'])
    
        
           
    
    return jsonify(newbook_list)





if __name__ == '__main__':
    app.run(debug=True)
