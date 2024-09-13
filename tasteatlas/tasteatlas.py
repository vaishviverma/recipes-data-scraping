from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import re


filename = "tasteatlas2.csv"
with open(filename, mode="w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["title","description","cuisine", "rating", "ingredient_list", "servings", "prep_time","cook_time", "rest_time", "ready_time", "source","steps","recipe_url","image_url"])

driver_path = 'chromedriver-linux64/chromedriver'
website = 'https://www.tasteatlas.com/recipes'
chrome_service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=chrome_service)

driver.get(website)

def get_title():
    try:
        title_element = driver.find_element(By.CLASS_NAME, 'h2.h2--large.h2--muli.h2--black.h2--capitalize.selected-variation-h2').text
    except:
        title_element = '-'
        
    return title_element

def get_description():  
    try:
        read_more_button = driver.find_element(By.XPATH, "//span[@class='read-more' and contains(text(), 'Read more')]")
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", read_more_button)
            time.sleep(1)
            read_more_button.click()
        except:
            pass
    except:
        print("Read more button not found.")
    
    try:
        des = driver.find_element(By.XPATH, "//div[@class='authentic-recipe__text ng-isolate-scope']/div[@class='read-more--hidden ng-scope']/p")
        desc = des.text
        desc = " ".join(desc.split())
    except:
        desc = '-'
        
    return desc

def get_ingredients():
    all_ingredients = []
    try:
        p_elements = driver.find_elements(By.XPATH, "//p[@class='ingredient-item']")
        for p in p_elements:
            all_ingredients.append(p.text) 
    except:
        pass
        
    return all_ingredients

def get_steps():
    all_steps = []
    try:
        div_elements = driver.find_elements(By.XPATH, "//div[@class='step-img-desc']")
        for div in div_elements:
            try:
                paragraph = div.find_element(By.TAG_NAME, 'p').text
                all_steps.append(paragraph) 
            except:
                pass
    except:
        pass
    return all_steps

def get_metadata():
    try:
        prep = driver.find_element(By.XPATH, "//div[@class='time-item preparation-time']").text
    except NoSuchElementException:
        prep = '-'
    try:
        cook = driver.find_element(By.XPATH, "//div[@class='time-item cook-time']").text
    except NoSuchElementException:
        cook = '-'
    try:
        ready = driver.find_element(By.XPATH, "//div[@class='time-item ready-time']").text
    except NoSuchElementException:
        ready = '-'
    try:
        rest = driver.find_element(By.XPATH, "//div[@class='time-item resting-time']").text
    except NoSuchElementException:
        rest = '-'
    
    return prep, cook, ready, rest


def get_image_url():
    try:
        image_element = driver.find_element(By.XPATH, "//div[@class='selected-variation-img-wrapper']")
        try:
            img = image_element.find_element(By.TAG_NAME, 'img')
            return img.get_attribute("src")
        except:
            return '-'
    except:
        print("Image element not found.")
        return '-'

def recipe_list():
    n = 66
    load_more_button_selector = '.btn.btn--inline.btn--underscore.btn--nopadding.btn--no-bgcolor.btn--black-text.btn--bold.hide-span-element'
    count = 0
    for _ in range(n):
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        
            load_more_button = driver.find_element(By.CSS_SELECTOR, load_more_button_selector)
            ActionChains(driver).move_to_element(load_more_button).click(load_more_button).perform()
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error: {e}")
            break
    time.sleep(15)
    
    try:
        div_elements = driver.find_elements(By.CLASS_NAME, 'details-heading__text')
        links = []

        for div in div_elements:
            try:
                a_tag = div.find_element(By.TAG_NAME, 'a')
                href = a_tag.get_attribute('href')
                if (count > 300):
                    links.append(href)
                count += 1
            except:
                pass
    except:
        pass

    return links

def get_rating():
    try:
        rating = driver.find_element(By.CSS_SELECTOR, 'p.rating-num.ng-binding.ng-scope').text
    except:
        rating = '-'
    return rating

def get_serving():
    try:
        serving_element = driver.find_element(By.XPATH, "//span[@class='ingredients-serving']")
        serving_text = serving_element.text
        return serving_text
    except:
        print("Serving information not found.")
        return '-'

def get_content(links):
    number_of_cuisines = 0
    
    for link in links:
        
        number_of_cuisines += 1
        driver.get(link)
        
        time.sleep(2)
        try:
            cuisine = driver.find_element(By.CLASS_NAME, 'subtitle.subtitle--location').text
        except:
            cuisine = '-'
        title = get_title()
        desc = get_description()
        preptime, cooktime, readytime, resttime = get_metadata()
        servings = get_serving()
        ingrd = get_ingredients()
        steps = get_steps()
        imageurl = get_image_url()
        recipeurl = driver.current_url
        rating = get_rating()
        store_output(title, desc, cuisine, rating, ingrd, servings, preptime, cooktime, resttime, readytime, steps, recipeurl, imageurl)                
    
def store_output(title, desc, cuisine, rating, ingrd, servings, preptime, cooktime, resttime, readytime, steps, recipeurl, imageurl):
    filename = "tasteatlas2.csv"
    data=[title, desc, cuisine, rating, ingrd, servings, preptime, cooktime, resttime, readytime, "TasteAtlas", steps, recipeurl, imageurl]
    with open(filename, mode="a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)
        
links = recipe_list()
get_content(links)

driver.quit()