from bs4 import BeautifulSoup
import grequests    #for async requests
import pandas as pd
import time

def get_urls():
    urls = []
    search_item = 'Hotel'           #you can change for your search
    location = 'London'             #change where you wanna search
    for x in range(0,10,10):
        urls.append("https://www.yelp.com/search?find_desc=" +search_item + "&find_loc="+location+"&start="+str(x))
    return urls

def get_data(urls):
    reqs = [grequests.get(link) for link in urls]
    time.sleep(0.15)
    resp = grequests.map(reqs, size=4)
    return resp

def parse(resp):
    business_page = []
    for r in resp:
        sp = BeautifulSoup(r.text, 'lxml')
        mains = sp.find_all('div', class_ = 'container__09f24__21w3G hoverable__09f24__2nTf3 margin-t3__09f24__5bM2Zmargin-b3__09f24__1DQ9x padding-t3__09f24__-R_5x padding-r3__09f24__1pBFG padding-b3__09f24__1vW6j padding-l3__09f24__1yCJfborder--top__09f24__8W8ca border--right__09f24__1u7Gt border--bottom__09f24__xdij8 border--left__09f24__rwKIa border-color--default__09f24__1eOdn')
        main_url = 'https://www.yelp.com'
        for main in mains:
            a_tag = main.find('a', class_ = 'css-166la90').get('href')
            a_tag_formated = main_url + str(a_tag)
            business_page.append(a_tag_formated)
            print('Added: ', a_tag_formated)
    return business_page


urls = get_urls()
resp = get_data(urls)
df = pd.DataFrame(parse(resp))
df.to_csv('Business page links.csv', index=False, header=False)
