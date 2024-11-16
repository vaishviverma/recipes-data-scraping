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

filename = "simplyrecipes.csv"
with open(filename, mode="w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["title","description","cuisine","ingredient_list","serving","prep_time","cook_time","total_time","source","steps","nutrients","recipe_url","image_url"])

driver_path = 'chromedriver-win32\\chromedriver.exe'
chrome_service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=chrome_service)

def get_title():
    try:
        title_element = driver.find_element(By.XPATH, "//h2[@id='recipe-block__header_1-0']").text
    except:
        title_element = '-'
    return title_element

def get_description():
    try:
        desc = driver.find_element(By.XPATH, "//p[@class='heading__subtitle']").text
        # inner_html = des.get_attribute('innerHTML')
        desc = re.sub(r'<br\s*\/?>', ' ', desc) 
        desc = re.sub(r'<.*?>', '', desc)
        desc = " ".join(desc.split())
    except: 
        desc = "-"
    return desc

def get_ingredients():
    all_ingredients = []
    try:
        ul_elements = driver.find_elements(By.XPATH, "//ul[@class='structured-ingredients__list text-passage']")
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
        uls = driver.find_elements(By.XPATH, "//ol//*[self::div[contains(@class, 'comp mntl-sc-block lifestyle-sc-block-subheading mntl-sc-block-subheading')] or self::p[contains(@class,'comp mntl-sc-block mntl-sc-block-html')]]")
        for ul in uls:
            all_steps.append(ul.text)
            
    except:
        pass
    return all_steps

def get_metadata():
    try:
        prep_time = driver.find_element(By.XPATH, "//div[@class='prep-time project-meta__prep-time']//span[@class='meta-text__data']").text
    except:
        prep_time = "-"
    try:
        cook_time = driver.find_element(By.XPATH, "//div[@class='cook-time project-meta__cook-time']//span[@class='meta-text__data']").text
    except:
        cook_time = "-"
    try:
        total_time = driver.find_element(By.XPATH, "//div[@class='total-time project-meta__total-time']//span[@class='meta-text__data']").text
    except:
        total_time = "-"
    try:        
        serves = driver.find_element(By.XPATH, "//div[@class='recipe-serving project-meta__recipe-serving']//span[@class='meta-text__data']").text
    except: 
        serves = "-"
    return prep_time, cook_time, total_time, serves

def get_image_url():
    try:
        image_element = driver.find_element(By.XPATH, "//img[@class='primary-image__image mntl-primary-image--blurry loaded']")
        img_src = image_element.get_attribute("src")
    except:
        img_src = "-"
    return img_src
    
def get_cuisine():
    try:
        cuisine = driver.find_element(By.XPATH, "//span[@class='wprm-recipe-cuisine wprm-block-text-bold']").text
    except:
        cuisine = "-"
    return cuisine

def get_nutrients():
    nutrients = []
    try:
        nutr = driver.find_elements(By.XPATH, "//tr[@class='nutrition-info__table--row']")
        for nu in nutr:
            ele = nu.find_elements(By.TAG_NAME,'td')
            um = [el.text for el in ele]
            um.reverse()
            nutrients.append(um)
    except:
        nutrients = []
    return nutrients

def get_content():
    with open('preprocessedlinks.txt', 'r') as file:
        for line in file:
            con = line.strip()
            driver.get(con)
            title = get_title()
            desc = get_description()
            preptime, cooktime, totaltime, serves = get_metadata()
            ingrd = get_ingredients()
            steps = get_steps()
            imageurl = get_image_url()
            recipeurl = driver.current_url
            cuisine = "-"
            nutrients = get_nutrients()
            store_output(title, desc, cuisine, ingrd, serves, preptime, cooktime, totaltime, steps, nutrients, recipeurl, imageurl)
          
def store_output(title, desc, cuisine, ingrd, serves, preptime, cooktime, totaltime, steps, nutrients, recipeurl, imageurl):
    filename = "simplyrecipes.csv"
    data=[title, desc, cuisine, ingrd, serves, preptime, cooktime, totaltime,"Simply Recipes", steps, nutrients, recipeurl, imageurl]
    with open(filename, mode="a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)


get_content()
driver.quit()


