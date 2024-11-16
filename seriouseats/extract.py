from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv

def setup(driver_path):
    chrome_service = Service(executable_path=driver_path)
    chrome_options = Options()
    chrome_options.add_argument("--disable-popup-blocking")
    return webdriver.Chrome(service=chrome_service, options=chrome_options)

driver = setup('chromedriver-linux64/chromedriver')

def get_title():
    try:
        container = driver.find_element(By.CLASS_NAME, 'recipe-decision-block__title')
        return container.text
    except:
        return "-"

def get_description():
    try:
        container = driver.find_element(By.CLASS_NAME, 'heading__subtitle')
        return container.text
    except:
        return "-"

def get_meta():
    try:
        container = driver.find_element(By.ID, "recipe-decision-block__container_1-0")
        label = container.find_elements(By.CLASS_NAME, 'meta-text__label')
        data = container.find_elements(By.CLASS_NAME, 'meta-text__data')
        labels = [i.text for i in label]
        data = [i.text for i in data]

        prep, cook, total, serves = "-", "-", "-", "-"

        for i in range(len(labels)):
            if labels[i] == "Prep":
                prep = data[i]
            if labels[i] == "Cook":
                cook = data[i]
            if labels[i] == "Total":
                total = data[i]
            if labels[i] == "Serves":
                serves = data[i]
        return prep, cook, total, serves
    except:
        return "-", "-", "-", "-"

def get_image():
    try:
        container = driver.find_element(By.CLASS_NAME, "primary-image__image")
        return container.get_attribute("src")
    except:
        return "-"

def get_rating():
    try:
        container = driver.find_element(By.ID, "aggregate-star-rating__stars_1-0")
        active_stars = container.find_elements(By.CSS_SELECTOR, 'a.active')
        return len(active_stars)
    except:
        return "-"

def get_ingredients():
    try:
        ingredients = driver.find_elements(By.CLASS_NAME, 'structured-ingredients__list-item')
        return [i.text for i in ingredients]
    except:
        return "-"

def get_instructions():
    try:
        instructions_elements = driver.find_elements(By.CSS_SELECTOR, 'ol.comp.mntl-sc-block > li.comp.mntl-sc-block')
        instructions = [instruction.find_element(By.CSS_SELECTOR, 'p.comp.mntl-sc-block-html').text for instruction in instructions_elements]
        return instructions
    except:
        return "-"

filename = "seriouseats2.csv"

def initialize():
    with open(filename, mode="w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["title","description","cuisine","rating","ingredient_list","serving","prep_time","cook_time","total_time", "source", "steps","recipe_url","image_url"])
        
def store_output(title, desc, cuisine, rating, ingrd, servings, preptime, cooktime, totaltime, steps, recipeurl, imageurl):
    data = [title, desc, cuisine, rating, ingrd, servings, preptime, cooktime, totaltime, "SeriousEats", steps, recipeurl, imageurl]
    with open(filename, mode="a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

initialize()
count = 0
with open("seriouseats/links.txt") as file:
    cuisine = "-"
    for link in file:

        if (link[0] == '#'):
            cuisine = link
            cuisine = ' '.join(cuisine.split()[:-2])
            cuisine = cuisine[1:]
            continue
        try:
            driver.get(link)
            time.sleep(2)
            prep, cook, total, serves = get_meta()
            title, desc, rating, ingrd, servings, preptime, cooktime, totaltime, steps, recipeurl, imageurl = (
                get_title(),
                get_description(),
                get_rating(),
                get_ingredients(),
                serves,
                prep,
                cook,
                total,
                get_instructions(),
                link.strip(),
                get_image()
            )
            store_output(title, desc, cuisine, rating, ingrd, servings, preptime, cooktime, totaltime, steps, recipeurl, imageurl)

        except:
            count += 1
            print('cant get', count)
    