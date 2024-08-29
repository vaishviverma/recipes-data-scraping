from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import csv
import re
import string

#recipe_title, description, cuisine, rating, ingredient_list, servings, prep_time, cook_time, total_time, source
# steps, recipe_url, image_url


filename = "bbc.csv"
with open(filename, mode="w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["title","description","cuisine","ingredient_list","serving","prep_time","cook_time","source","steps","recipe_url","image_url"])

driver_path = 'chromedriver-win32\chromedriver.exe'
website = 'https://www.bbc.co.uk/food/cuisines'
chrome_service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=chrome_service)

driver.get(website)


def get_title():
    try:
        title_element = driver.find_element(By.XPATH, "//h1[@class='gel-trafalgar content-title__text']")
    except:
        title_element = '-'
    return title_element.text

def get_description():
    try:
        des = driver.find_element(By.XPATH, "//p[@class='recipe-description__text']")
        inner_html = des.get_attribute('innerHTML')
        desc = re.sub(r'<br\s*\/?>', ' ', inner_html) 
        desc = re.sub(r'<.*?>', '', desc)
        desc = " ".join(desc.split())
    except: 
        desc = "-"
    return desc

def get_ingredients():
    all_ingredients = []
    try:
        ul_elements = driver.find_elements(By.XPATH, "//ul[@class='recipe-ingredients__list']")
        for ul in ul_elements:
            li_elements = ul.find_elements(By.TAG_NAME, 'li')
            ingredients = [li.text for li in li_elements]
            all_ingredients.extend(ingredients) 
    except:
        pass
    return all_ingredients

def get_steps():
    all_steps = []
    try:
        ul = driver.find_element(By.XPATH, "//ol[@class='recipe-method__list']")
        li_elements = ul.find_elements(By.TAG_NAME, 'li')
        step = [li.text for li in li_elements]
        all_steps.extend(step) 
    except:
        pass
    return all_steps

def get_metadata():
    try:
        prep_time = driver.find_elements(By.XPATH, "//p[@class='recipe-metadata__prep-time']")[-1].text
        cook_time = driver.find_elements(By.XPATH, "//p[@class='recipe-metadata__cook-time']")[-1].text
        serves = driver.find_elements(By.XPATH, "//p[@class='recipe-metadata__serving']")[-1].text
    except: 
        pass
    return prep_time, cook_time, serves


def get_image_url():
    try:
        image_element = driver.find_element(By.XPATH, "//div[@class='recipe-media__image responsive-image-container__16/9']")
        img = image_element.find_element(By.TAG_NAME, 'img')
        return img.get_attribute("src")
    except NoSuchElementException:
        print("Image element not found.")
        return None
    
def get_rating():
    try:
        rating = driver.find_element(By.XPATH, "//span[contains(@class, 'aggregate-rating__total') and contains(@class, 'gel-long-primer-bold')]").text
    except:
        rating = '-'
    return rating

cuisine = ["british","african","american","italian","indian","caribbean","chinese","east_european","french","greek","irish","japanese","korean","mexican",
           "nordic","pakistani","north_african","portuguese","south-american","spanish","turkish_and_middle_eastern","thai_and_south-east_asian"]


links=[]

def get_cuisine():
    for i in cuisine:
        for letter in string.ascii_lowercase:
            try:
                url = "https://www.bbc.co.uk/food/cuisines/"+ i +"/a-z/" + letter
                driver.get(url)
                if driver.current_url == ("https://www.bbc.co.uk/food/cuisines/"+i):
                    driver.back()
                    continue
                flag = True
                while flag==True:
                    elements = driver.find_elements(By.XPATH,"//div[@class='gel-layout__item gel-1/2 gel-1/3@m gel-1/4@xl']")
                    for ele in elements:
                        links.append(ele.find_element(By.TAG_NAME,'a').get_attribute("href"))

                    try:
                        next_page = driver.find_elements(By.XPATH,"//li[@class='pagination__list-item pagination__priority--0']")
                        page = next_page[-1].find_element(By.TAG_NAME,'a')
                        if page.get_attribute("href")!=driver.current_url:
                            driver.get(page.get_attribute("href"))
                    except:
                        print("no next page")
                        flag=False
                    
            except:
                print("no recipe with this letter")

def store_output(title, desc, cuisine, rating, ingrd, serves, preptime, cooktime, steps, recipeurl, imageurl):
    filename = "bbc.csv"
    data=[title, desc, cuisine, rating, ingrd, serves, preptime, cooktime, "BBC Food", steps, recipeurl, imageurl]
    with open(filename, mode="a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def store_links(links):
    with open('links.txt', 'w') as file:
        for link in links:
            file.write(link+"\n")

get_cuisine()
store_links(links)

driver.quit()