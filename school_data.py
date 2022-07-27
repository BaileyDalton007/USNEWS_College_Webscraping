from selenium import webdriver

from bs4 import BeautifulSoup

LINK = 'https://www.usnews.com/best-colleges/'

PAGES = ['overall-rankings', 'applying', 'academics', 'student-life', 'paying']

def get_html(href):
    driver = webdriver.Firefox()
    extension_path = 'adblocker_ultimate.xpi'
    driver.install_addon(extension_path, temporary=True)

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
    third_table = soup.findAll('a', attrs={'class': 'Anchor-byh49a-0 PlBer'})

    data.append(int(rank.contents[0].contents[0].replace('#', '')))

    for tag in first_table:
        data.append(tag.contents[0])

    # Only shows public or private
    data[2] = data[2].split(',')[0]

    labels = ['median starting salary of alumni', '4-year graduation rate',
            'collegiate athletic association']

    out = {}
    for i, label_tag in enumerate(third_table):
        if str(label_tag.contents[0]).lower() in labels:
            t = str(label_tag.contents[0]).lower()
            out[t] = third_table[i + 1].contents[0]

    try:
        data.append(out['median starting salary of alumni'])
    except:
        data.append('N/A')
    try:
        data.append(out['4-year graduation rate'])
    except:
        data.append('N/A')
    try:
        data.append(out['collegiate athletic association'])
    except:
        data.append('N/A')

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

    # SAT scores
    try:
        second_table = soup.find('div', attrs={'class': 'BarChartStacked__Legend-wgxhoq-4 iLdLaQ'})
        sat_ranges = second_table.findAll('div')

        #print(sat_ranges[2].contents[1:])
        s_range = []
        s_dist = []
        for score in sat_ranges:
            s_range.append(score.contents[1])
            s_dist.append(score.contents[2].contents[0])

        res = dict(zip(s_range, s_dist))
        data.append(res['1400-1600'])
        data.append(res['1200-1399'])
        data.append(res['1000-1199'])
        data.append(res['800-999'])
        data.append(res['600-799'])
        data.append(res['400-599'])
    except:
        # Adds 'N/A' values to fill SAT score columns if scores not found
        for i in range(6):
            data.append('N/A')


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

    try:
        second_table = soup.findAll('p', attrs={'class': 'Paragraph-sc-1iyax29-0 kGlRjY'})

        labels = ['typical total federal loan debt after graduation', 'typical total federal loan debt among those who did not graduate']
        out = {}
        for i, tag in enumerate(second_table):
            t = tag.find('span', attrs={'class': 'Span-sc-19wk4id-0 fgWqyH'})
            
            if t is not None and str(t.contents[0]).lower() in labels:
                t = str(t.contents[0]).lower()
                out[t] = second_table[i + 1].contents[0]
        
        
        data.append(out['typical total federal loan debt after graduation'])
        data.append(out['typical total federal loan debt among those who did not graduate'])
    except:

        # Fills columns if no values are found
        data.append('N/A')
        data.append('N/A')

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