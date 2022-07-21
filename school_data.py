from turtle import get_shapepoly
from selenium import webdriver

from bs4 import BeautifulSoup

LINK = 'https://www.usnews.com/best-colleges/'

PAGES = ['overall-rankings', 'applying', 'academics', 'student-life', 'paying']

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
def overview_page(data, href):
    soup = BeautifulSoup(get_html(href), 'html.parser')

    rank = soup.find('span', attrs={'class': 'ProfileHeading__RankingSpan-sc-1n3m2r3-6 dssRIi'})

    first_table = soup.findAll('p', attrs={'class': 'Paragraph-sc-1iyax29-0 clmBuI'})

    second_table = soup.findAll('p', attrs={'class': 'Paragraph-sc-1iyax29-0 Section__ParagraphStyled-ply21t-4 eRvRyE jTHqXR'})

    data.append(int(rank.contents[0].contents[0].replace('#', '')))

    for tag in first_table:
        data.append(tag.contents[0])

    # Only shows public or private
    data[2] = data[2].split(',')[0]
    
    data_2 = []
    for tag in second_table:
        data_2.append(tag.contents[0])


########################## Rankings Page ##########################

def rankings_page(data, href):
    soup = BeautifulSoup(get_html(href + '/' + PAGES[0]), 'html.parser')

    first_table = soup.findAll('p', attrs={'class': 'Paragraph-sc-1iyax29-0 eRvRyE'})

    for tag in first_table:
        data.append(tag.contents[0])

########################## Admissions Page ##########################

def admissions_page(data, href):
    soup = BeautifulSoup(get_html(href + '/' + PAGES[1]), 'html.parser')

    first_table = soup.findAll('dd', attrs={'class': 'QuickStat__Description-sc-1m0tve6-1 dpatpE QuickStat-sc-1m0tve6-3 fWFpaK QuickStat-sc-1m0tve6-4 eMJrp'})

    for tag in first_table:
        data.append(tag.contents[0])

########################## Student Life Page ##########################

def student_life_page(data, href):

    soup = BeautifulSoup(get_html(href + '/' + PAGES[3]), 'html.parser')

    first_table = soup.findAll('span', attrs={'class': 'Span-sc-19wk4id-0 dFGiyP'})

    for i in range(3):
        data.append(first_table[i].contents[0])

########################## Tuition and Aid Page ##########################

def tuition_page(data, href):

    soup = BeautifulSoup(get_html(href + '/' + PAGES[4]), 'html.parser')

    first_table = soup.findAll('span', attrs={'class': 'Span-sc-19wk4id-0 dFGiyP'})

    for i in range(2):
        data.append(first_table[i].contents[0])

########################## Execution ##########################

def get_school_data(name, href):
    SCHOOL_HREF = href

    data = [name]
    overview_page(data, SCHOOL_HREF)
    rankings_page(data, SCHOOL_HREF)
    admissions_page(data, SCHOOL_HREF)
    student_life_page(data, SCHOOL_HREF)
    tuition_page(data, SCHOOL_HREF)

    for i, d in enumerate(data):
        data[i] = to_float(d)

    return data
