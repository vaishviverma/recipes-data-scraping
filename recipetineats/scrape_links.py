from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv

#basic setup for selenium

def setup(driver_path):
    # setup chrome driver service and options
    chrome_service = Service(executable_path=driver_path)
    chrome_options = Options()
    chrome_options.add_argument("--disable-popup-blocking")
    return webdriver.Chrome(service=chrome_service, options=chrome_options)


def store_links(links):

    with open('links.txt', 'w') as file:
        for link in links:
            file.write(link[0]+","+link[1]+"\n")


links = []
url = 'https://www.recipetineats.com/recipes/?fwp_paged='

driver = setup('chromedriver-linux64/chromedriver')

for i in range(1,79):
    driver.get(url+str(i))
    ele = driver.find_element(By.XPATH, "//main[@class='content facetwp-template']")
    art = ele.find_elements(By.TAG_NAME, 'article')
    for ar in art:
        a = ar.find_element(By.TAG_NAME, 'a')
        link = a.get_attribute("href")
        print(link)
        links.append(link)

store_links(links)

driver.quit()