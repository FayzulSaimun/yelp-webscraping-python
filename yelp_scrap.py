import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup


#making a chrome drive and adding chrome driver options
options = Options()
options.page_load_strategy = 'eager'
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=options)


all_page_urls = []     #to save the page urls
business_pages =[]     #to save the business page url

search_item = 'Hotel'  #you can change what your wanna search for
location = 'London'    #change in which loaction you want to search

base_url = "https://www.yelp.com/search?find_desc=" +search_item + "&find_loc="+location+"&start="  #main search page urls pattern

def yelp_search_link():
  for i in range(0,200,10):       #change here for your requirement
    main_url = base_url+str(i)
    all_page_urls.append(main_url)
    print(main_url)
yelp_search_link()

def find_items_page():               #finding all business pages urls from main search page
    for urls in all_page_urls:
        browser.get(urls)
        time.sleep(1)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        time.sleep(0.30)
        mains = soup.find_all('div', class_ = 'container__09f24__21w3G hoverable__09f24__2nTf3 margin-t3__09f24__5bM2Z margin-b3__09f24__1DQ9x padding-t3__09f24__-R_5x padding-r3__09f24__1pBFG padding-b3__09f24__1vW6j padding-l3__09f24__1yCJf border--top__09f24__8W8ca border--right__09f24__1u7Gt border--bottom__09f24__xdij8 border--left__09f24__rwKIa border-color--default__09f24__1eOdn')
        main_url = 'https://www.yelp.com'
        for main in mains:
            a_tag = main.find('a', class_ = 'css-166la90').get('href')
            a_tag_formated = main_url + str(a_tag)
            items_pages.append(a_tag_formated)
            print(a_tag_formated)
find_items_page()

Names = []            #Name of the business profile
Reviews = []          #No of reviews recieved
Open_Hour = []        #Open hours
Price_range = []      #Price range
Address = []          #Address of the business
Websites = []         #Wbsites of the business
Phones = []           #Phone number of the business


def scrape_and_save():
    for url in business_pages:
        browser.get(url)
        ss = BeautifulSoup(browser.page_source, 'html.parser')
        mainPage = ss.find('div', class_ = 'main-content-wrap main-content-wrap--full')    #main content

        try:
            name = mainPage.find('h1', class_ = 'css-11q1g5y').get_text()
            Names.append(name)
        except AttributeError:
            name = 'NUll'
            Names.append(name)

        try:
            review = mainPage.find('span', class_ = 'css-bq71j2').get_text()
            Reviews.append(review)
        except AttributeError:
            review = 'Null'
            Reviews.append(review)

        try:
            price = mainPage.find('span', class_ = 'css-1xxismk').get_text()
            Price_range.append(price)
        except AttributeError:
            price = 'Null'
            Price_range.append(price)

        try:
            opens = mainPage.find('div', class_="display--inline-block__373c0__2de_K margin-r1-5__373c0__1Vie3 border-color--default__373c0__2oFDT").
            find_next('span', class_ = 'css-bq71j2').get_text()
            Open_Hour.append(opens)
        except AttributeError:
            opens = 'Null'
            Open_Hour.append(opens)

        try:
            address = mainPage.find('div', class_ = 'css-1vhakgw border--top__373c0__19Owr border-color--default__373c0__2oFDT').
            find_next('p', class_ = 'css-1h1j0y3').find_next('p', class_ = 'css-e81eai').get_text()
            Address.append(address)
        except AttributeError:
            address = 'Null'
            Address.append(address)
        except TypeError:
            address = 'Null'
            Address.append(address)

        try:
            website = mainPage.find('a', class_ = 'css-ac8spe').get_text()
            website = 'https://www.'+ str(website)
            Websites.append(website)
        except AttributeError:
            website = 'Null'
            Websites.append(website)

        try:
            phone = mainPage.find('div', class_ = 'stickySidebar__373c0__3PY1o border-color--default__373c0__2oFDT').
            find('p', class_ = 'css-1h1j0y3').find_next('p', class_ = 'css-1h1j0y3').get_text()
            Phones.append(phone)
        except AttributeError:
            phone = 'Null'
            Phones.append(phone)

        print('Scraping Compeleted',url)

    df = pd.DataFrame({'Names':Names, 'Price Range': Price_range, 'Reviews': Reviews,
                       'Address':Address, 'Website': Websites,'Phone Number': Phones})  #making a pandas dataframe
    
    df.to_csv('Business Data.csv')   #Saving the data as csv
    
scrape_and_save()
    
