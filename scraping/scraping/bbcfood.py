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

#recipe_title, description, cuisine, ingredient_list, servings, prep_time, cook_time, total_time, source
# steps, recipe_url, image_url


filename = "output.csv"
with open(filename, mode="w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["title","description","cuisine","ingredient_list","serving","prep_time","cook_time","source","steps","recipe_url","image_url"])

driver_path = 'chromedriver-win32\chromedriver.exe'
website = 'https://www.bbc.co.uk/food/cuisines'
chrome_service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=chrome_service)

driver.get(website)


def get_title():
    title_element = driver.find_element(By.XPATH, "//h1[@class='gel-trafalgar content-title__text']")
    return title_element.text

def get_description():
    des = driver.find_element(By.XPATH, "//p[@class='recipe-description__text']")
    inner_html = des.get_attribute('innerHTML')
    desc = re.sub(r'<br\s*\/?>', ' ', inner_html) 
    desc = re.sub(r'<.*?>', '', desc)
    desc = " ".join(desc.split())
    return desc

def get_ingredients():
    all_ingredients = []
    ul_elements = driver.find_elements(By.XPATH, "//ul[@class='recipe-ingredients__list']")
    for ul in ul_elements:
        li_elements = ul.find_elements(By.TAG_NAME, 'li')
        ingredients = [li.text for li in li_elements]
        all_ingredients.extend(ingredients) 
    return all_ingredients

def get_steps():
    all_steps = []
    ul = driver.find_element(By.XPATH, "//ol[@class='recipe-method__list']")
    li_elements = ul.find_elements(By.TAG_NAME, 'li')
    step = [li.text for li in li_elements]
    all_steps.extend(step) 
    return all_steps

def get_metadata():
    prep_time_element = driver.find_elements(By.XPATH, "//p[@class='recipe-metadata__prep-time']")
    cook_time_element = driver.find_elements(By.XPATH, "//p[@class='recipe-metadata__cook-time']")
    serve_element = driver.find_elements(By.XPATH, "//p[@class='recipe-metadata__serving']")
    for p in prep_time_element:
        preparation_time = p.text
    for c in cook_time_element:
        cooking_time = c.text
    for s in serve_element:
        serves = s.text
    return preparation_time, cooking_time, serves


def get_image_url():
    try:
        image_element = driver.find_element(By.XPATH, "//div[@class='recipe-media__image responsive-image-container__16/9']")
        img = image_element.find_element(By.TAG_NAME, 'img')
        return img.get_attribute("src")
    except NoSuchElementException:
        print("Image element not found.")
        return None

def get_cuisine():
    cuisine_elements = driver.find_elements(By.XPATH,"//a[@class='promo promo__cuisine']")
    cuisine_dict = {}

    for ele in cuisine_elements:
        cuisine_name = ele.find_element(By.TAG_NAME,"h3")
        cuisine_dict[cuisine_name.text] = ele.get_attribute("href")
    
    number_of_cuisines = 0
    for i in cuisine_dict:
            cuisine=i
            driver.get(cuisine_dict[i])
            dishes = driver.find_elements(By.XPATH,"//a[@class='promo promo__main_course']")
            links=[]
            for dish in dishes:
                links.append(dish.get_attribute("href"))
            number_of_cuisines+=1
            if number_of_cuisines>4:
                break
            count=0
            for i in range(5):
                driver.get(links[i])
                title = get_title()
                desc = get_description()
                preptime, cooktime, serves = get_metadata()
                ingrd = get_ingredients()
                steps = get_steps()
                imageurl = get_image_url()
                recipeurl = driver.current_url
                store_output(title, desc, cuisine, ingrd, serves, preptime, cooktime, steps, recipeurl, imageurl)
                count+=1
                if count>5:
                    break
                driver.back()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='promo promo__main_course']")))

            driver.back()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='promo promo__cuisine']")))
            


def store_output(title, desc, cuisine, ingrd, serves, preptime, cooktime, steps, recipeurl, imageurl):
    filename = "output.csv"
    data=[title, desc, cuisine, ingrd, serves, preptime, cooktime, "BBC Food", steps, recipeurl, imageurl]
    with open(filename, mode="a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)
        

get_cuisine()

driver.quit()