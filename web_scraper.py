from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver import FirefoxOptions
from school_data import get_school_data

import csv

from bs4 import BeautifulSoup

import time

options = FirefoxOptions()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'
options.add_argument('user-agent={0}'.format(user_agent))

driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 20)
action = ActionChains(driver)

driver.get("https://www.usnews.com/best-colleges/rankings/national-universities")
driver.delete_all_cookies()

while True:
    try:
        element = driver.find_element('css selector', '.pager__ButtonStyled-sc-1i8e93j-1')
        driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()
        time.sleep(1.5)
    except:
        break

html = driver.page_source
time.sleep(2)

# close web browser
driver.close()

soup = BeautifulSoup(html, 'html.parser')

tags = soup.findAll('a', attrs={'class': 'Anchor-byh49a-0 DetailCardCollegesAtlas__StyledAnchor-sc-19muj1z-8 PlBer hOvOgG card-name'})

uni_names = []
uni_hrefs = []

for tag in tags:
    uni_names.append(tag.contents[0])
    uni_hrefs.append(tag['href'])

# The rest of the schools are not ranked.
uni_names = uni_names[:297]
uni_hrefs = uni_hrefs[:297]

csv_file = open('college_data.csv', 'w+', newline='')
csv_writer = csv.writer(csv_file)


column_names = ['name', 'rank', 'type', 'founded', 'religon', 'schedule', 'location_type', 'phone_num',
                'alumni_sal','four_year_grad_rate', 'sport_assoc',
                'usnews_score', 'six_year_grad_rate', 'six_year_with_pell', 'six_year_without_pell',
                'percent_class_less_twenty', 'percent_class_more_fifty', 'student_to_fac', 'app_deadline',
                'app_fee', 'acceptance_rate', 'sat_1400-1600', 'sat_1200-1399', 'sat_1000-1199', 'sat_800-999', 'sat_600-799', 'sat_400-599', 'total_enroll', 'undergrad_enroll', 'grad_enroll', 'tuition',
                'room_and_board', 'fed_debt', 'fed_debt_not_grad']

csv_writer.writerow(column_names)

for (name, href) in zip(uni_names, uni_hrefs):
    new_row = get_school_data(name, href)

    csv_writer.writerow(new_row)

csv_file.close()