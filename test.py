from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver import FirefoxOptions

from bs4 import BeautifulSoup

import time

LINK = 'https://www.usnews.com/best-colleges/'
SCHOOL_HREF = 'princeton-university-2627'

PAGES = ['overall-rankings', 'applying', 'academics', 'student-life', 'paying']

data = []

def get_values(values_to_get, raw_data):
    for value in values_to_get:
        index = raw_data.index(value) + 1
        d = raw_data[index]
        try:
            d = d.contents[0]
        except:
            pass
        
        data.append(d)

def get_html(href):
    ## Some documentation say this is needed- but in my case just slowed down get requests
    #options = FirefoxOptions()
    #user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
    #options.add_argument('user-agent={0}'.format(user_agent))
    #driver = webdriver.Firefox(options=options)


    driver = webdriver.Firefox()

    driver.get(LINK + href)
    driver.delete_all_cookies()

    html = driver.page_source
    
    # Close web browser
    driver.close()
    
    return html

def to_float(str):
    try:
        p = str.replace('$', '')
        p = p.replace('%', '')
        p = p.replace(',', '')
        return float(p)
    except:
        return str

########################## Overview Page ##########################
def overview_page():
    soup = BeautifulSoup(get_html(SCHOOL_HREF), 'html.parser')

    rank = soup.find('span', attrs={'class': 'ProfileHeading__RankingSpan-sc-1n3m2r3-6 dssRIi'})

    first_table = soup.findAll('p', attrs={'class': 'Paragraph-sc-1iyax29-0 clmBuI'})

    second_table = soup.findAll('a', attrs={'class': 'Anchor-byh49a-0 PlBer'})

    third_table = soup.findAll('p', attrs={'class': 'Paragraph-sc-1iyax29-0 Section__ParagraphStyled-ply21t-4 eRvRyE jTHqXR'})

    data.append(int(rank.contents[0].contents[0].replace('#', '')))

    for tag in first_table:
        data.append(tag.contents[0])

    # Only shows public or private
    data[1] = data[1].split(',')[0]

    data_2 = []
    for tag in second_table:
        data_2.append(tag.contents[0])

    values_to_get = ["Median starting salary of alumni", "4-year graduation rate",
                        "Tuition and fees", "Room and board", "Health insurance offered"]

    get_values(values_to_get, data_2)

    
    data_3 = []
    for tag in third_table:
        data_3.append(tag.contents[0])

    # Total enrollment
    data.append(data_3[0])

########################## Rankings Page ##########################

def rankings_page():
    soup = BeautifulSoup(get_html(SCHOOL_HREF + '/' + PAGES[0]), 'html.parser')

    first_table = soup.findAll('p', attrs={'class': 'Paragraph-sc-1iyax29-0 eRvRyE'})

    for tag in first_table:
        data.append(tag.contents[0])

########################## Admissions Page ##########################

def admissions_page():
    soup = BeautifulSoup(get_html(SCHOOL_HREF + '/' + PAGES[1]), 'html.parser')

    first_table = soup.findAll('dd', attrs={'class': 'QuickStat__Description-sc-1m0tve6-1 dpatpE QuickStat-sc-1m0tve6-3 fWFpaK QuickStat-sc-1m0tve6-4 eMJrp'})

    for tag in first_table:
        data.append(tag.contents[0])

########################## Student Life Page ##########################

def student_life_page():

    soup = BeautifulSoup(get_html(SCHOOL_HREF + '/' + PAGES[3]), 'html.parser')

    first_table = soup.findAll('span', attrs={'class': 'Span-sc-19wk4id-0 dFGiyP'})

    for i in range(3):
        data.append(first_table[i].contents[0])

########################## Execution ##########################

def get_school_data(name, href):
    overview_page()
    rankings_page()
    admissions_page()
    student_life_page()

    for i, d in enumerate(data):
        data[i] = to_float(d)

    return data