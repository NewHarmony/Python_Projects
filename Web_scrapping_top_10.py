# Udemy Course ZTM Python HackerNews Webscrapping Project
#my modifications: 
# 1. Request no. of pages to check
# 2. Checks if pages exist and if there are links on that page
# 3. Collect data from the pages return the 10 most popular articles

import requests
from bs4 import BeautifulSoup
import pprint


first_page = 'https://news.ycombinator.com/news'
next_page = 'https://news.ycombinator.com/news?p='


def page_list_fun(max_page_no):
    page_list = []
    i = 1
    while i < (max_page_no + 1):
        page_list.append(next_page +str(i))
        i+=1
    return fun(page_list)


def fun(page_list) :
    mega_links = []
    mega_subtext = []

    for page in page_list:
        res = requests.get(page)
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.storylink')
        subtext = soup.select('.subtext')
        mega_links += links
        mega_subtext += subtext  
    return top_ten_articles(mega_links, mega_subtext)


def top_ten_articles(mega_links, mega_subtext):
    articles = []
    for idx, item in enumerate(mega_links):
        title = item.getText()
        #print(title)
        href = item.get('href', None)
        vote = mega_subtext[idx].select('.score')

        if len(vote):
            votes = int(vote[0].getText().replace(' points', ''))
            articles.append({'title': title, 'link': href, 'points': votes})
    top_ten = sorted(articles, key=lambda x: x['points'], reverse = True)[:10]
    return pprint.pprint(top_ten)


while True:
    try:
        max_page_no = input("Please enter max page number? ")
        last_page = next_page + str(max_page_no)
        res = requests.get(last_page)
        #requests.get(last_page)

        try:
            max_page_no = int(max_page_no)
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.select('.storylink')
            subtext = soup.select('.subtext') 

            if links != []:
                print("Compiling page list")
                page_list_fun(max_page_no)
                break
            
            elif links == []:
                print("Sorry, no links were found on this page.")
                break

        except:
            print("You need to enter a number.")
            break

    except requests.exceptions.RequestException as err:
        print("Sorry, page does not exist")
        raise SystemExit(err)
