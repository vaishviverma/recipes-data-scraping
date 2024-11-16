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

filename = "dassana.csv"
with open(filename, mode="w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["title","description","cuisine","rating","ingredient_list","serving","prep_time","cook_time","total_time","source","steps","nutrients","recipe_url","image_url"])

driver_path = 'chromedriver-win32\\chromedriver.exe'
chrome_service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=chrome_service)

def get_title():
    try:
        title_element = driver.find_element(By.XPATH, "//h2[@class='wprm-recipe-name wprm-block-text-normal']").text
    except:
        title_element = '-'
    return title_element

def get_description():
    try:
        desc = driver.find_element(By.XPATH, "//div[@class='wprm-recipe-summary wprm-block-text-normal']").text
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
        ul_elements = driver.find_elements(By.XPATH, "//ul[@class='wprm-recipe-ingredients']")
        for ul in ul_elements:
            li_elements = ul.find_elements(By.TAG_NAME, 'li')
            ingredients = [li.text[2:] for li in li_elements]
            all_ingredients.extend(ingredients) 
    except:
        pass
    return all_ingredients

def get_steps():
    all_steps = []
    try:
        ul = driver.find_elements(By.XPATH, "//ul[@class='wprm-recipe-instructions']")
        for u in ul:
            li_elements = u.find_elements(By.TAG_NAME, 'li')
            for li in li_elements:
                step = li.text
                step = re.sub(r'<br\s*\/?>', ' ', step) 
                step = re.sub(r'<.*?>', '', step)
                step = " ".join(step.split())
                all_steps.append(step)
            # step = [li.text for li in li_elements]
            # all_steps.extend(step) 
    except:
        pass
    return all_steps

def get_metadata():
    try:
        prep_time = driver.find_element(By.XPATH, "//span[@class='wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-prep_time wprm-recipe-prep_time-minutes']").text.replace("\n"," ")
    except:
        prep_time = "-"
    try:
        cook_time = driver.find_element(By.XPATH, "//span[@class='wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-cook_time wprm-recipe-cook_time-minutes']").text.replace("\n"," ")
    except:
        cook_time = "-"
    try:
        total_time = driver.find_element(By.XPATH, "//span[@class='wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-total_time wprm-recipe-total_time-minutes']").text.replace("\n"," ")
    except:
        total_time = "-"
    try:        
        serves = driver.find_element(By.XPATH, "//div[@class='wprm-recipe-ingredients-servings']").find_element(By.TAG_NAME, 'input').get_attribute("value")
    except: 
        serves = "-"
    
    return prep_time, cook_time, total_time, serves

def get_image_url():
    try:
        image_element = driver.find_element(By.XPATH, "//div[@class='wp-block-image']")
        driver.execute_script("arguments[0].scrollIntoView();", image_element)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))

        img_el = image_element.find_element(By.TAG_NAME, 'img')

        img_src = img_el.get_attribute("src")

        if "data:image/svg+xml" in img_src or "placeholder" in img_src:
            img_src = img_el.get_attribute("data-src") or img_el.get_attribute("data-lazy-src") or img_el.get_attribute("data-srcset")
    except:
        img_src = "-"
    return img_src
    
def get_rating():
    try:
        rating = driver.find_element(By.XPATH, "//div[@class='wprm-recipe-rating-details wprm-block-text-normal']//span[@class='wprm-recipe-rating-average']").text
    except:
        rating = '-'
    return rating

def get_cuisine():
    try:
        cuisine = driver.find_element(By.XPATH, "//span[@class='wprm-recipe-cuisine wprm-block-text-bold']").text
    except:
        cuisine = "-"
    return cuisine

def get_content():
    with open('dassanalinks.txt', 'r') as file:
        for _ in range(694):
            file.readline()
        for line in file:
            driver.get(line)
            title = get_title()
            desc = get_description()
            preptime, cooktime, totaltime, serves = get_metadata()
            ingrd = get_ingredients()
            steps = get_steps()
            imageurl = get_image_url()
            recipeurl = driver.current_url
            rating = get_rating()
            cuisine = get_cuisine()
            nutrients = get_nutrients()
            store_output(title, desc, cuisine, rating, ingrd, serves, preptime, cooktime, totaltime, steps, nutrients, recipeurl, imageurl)

def store_output(title, desc, cuisine, rating, ingrd, serves, preptime, cooktime, totaltime, steps, nutrients, recipeurl, imageurl):
    filename = "dassana.csv"
    data=[title, desc, cuisine, rating, ingrd, serves, preptime, cooktime, totaltime,"Dassana's Veg Recipes", steps, nutrients, recipeurl, imageurl]
    with open(filename, mode="a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def store_links(links):
    with open('dassanalinks.txt', 'w') as file:
        for link in links:
            file.write(link+"\n")

def get_nutrients():
    Nutrients = []

    main = driver.find_elements(By.XPATH, "//span[@class='nutrition-main']")
    for el in main:
        Nutrients.append([el.text])
    sub = driver.find_elements(By.XPATH, "//span[@class='nutrition-sub']")
    for el in sub:
        Nutrients.append([el.text])
    return Nutrients

# there is a dassanalinks.txt file where all the links of recipes are saved
get_content()

driver.quit()