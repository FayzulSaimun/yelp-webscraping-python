from bs4 import BeautifulSoup
import grequests
import pandas as pd
import time

start = time.perf_counter()

def get_data():
    reqs = [grequests.get(link) for link in (open('Business_page_links.csv').readlines())]
    time.sleep(0.23)
    resp = grequests.map(reqs, size = 5)
    return resp

def parse(resp):
    Names = []
    Reviews = []
    Price_range = []
    Open_Hour = []
    Address = []
    Websites = []
    Phones = []
    for r in resp:
        soup = BeautifulSoup(r.text, 'lxml')
        time.sleep(0.22)
        mainPage = soup.find('div', class_ = 'main-content-wrap main-content-wrap--full')

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
            opens = mainPage.find('div', class_="display--inline-block__373c0__2de_K margin-r1-5__373c0__1Vie3 border-color--default__373c0__2oFDT").find_next('span', class_ = 'css-bq71j2').get_text()
            Open_Hour.append(opens)
        except AttributeError:
            opens = 'Null'
            Open_Hour.append(opens)

        try:
            address = mainPage.find('div', class_ = 'css-1vhakgw border--top__373c0__19Owr border-color--default__373c0__2oFDT').find_next('p', class_ = 'css-1h1j0y3').find_next('p', class_ = 'css-e81eai').get_text()
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
            phone = mainPage.find('div', class_ = 'stickySidebar__373c0__3PY1o border-color--default__373c0__2oFDT').find('p', class_ = 'css-1h1j0y3').find_next('p', class_ = 'css-1h1j0y3').get_text()
            Phones.append(phone)
        except AttributeError:
            phone = 'Null'
            Phones.append(phone)

        print(r)
        print('Added:', name)
    df = pd.DataFrame({'Names':Names, 'Price Range': Price_range, 'Open Hours':Open_Hour, 'Reviews': Reviews, 'Address':Address, 'Website': Websites,'Phone Number': Phones})
    df.to_csv('Business_Data_async.csv', index=False)

resp = get_data()
parse(resp)
end = time.perf_counter()
print('Time taken:', end-start)
