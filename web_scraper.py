from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver import FirefoxOptions

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

print(uni_names)
print(uni_hrefs)