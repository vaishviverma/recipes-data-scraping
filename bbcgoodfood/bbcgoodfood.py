from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from bs4 import BeautifulSoup
import csv
import re
from selenium.webdriver.chrome.options import Options

# recipe_title, description, cuisine, rating, ingredient_list, servings, prep_time, cook_time, total_time, source, steps, recipe_url, image_url

filename = "bbcgoodfood.csv"
with open(filename, mode="w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["title","description","cuisine","rating","ingredient_list","serving","prep_time","cook_time","source","steps","recipe_url","image_url", "kcal", "fat", "saturates", "carbs", "sugars", "fibre", "protein", "salt" ])

driver_path = 'chromedriver-win32\\chromedriver.exe'
chrome_service = Service(executable_path=driver_path)
chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

def get_nutrients():
    #kcal, fat, saturates, carbs, sugars, fibre, protein, salt
    try:
        nutrients = driver.find_element(By.XPATH, "//table[@class='key-value-blocks hidden-print mt-xxs']")
        nutr = nutrients.find_elements(By.TAG_NAME, 'tbody')
        uh = nutr[0].find_elements(By.XPATH,"//td[@class='key-value-blocks__value']")
        kcal, fat, saturates, carbs = uh[0].text, uh[1].text, uh[2].text, uh[3].text
        uh = nutr[1].find_elements(By.XPATH,"//td[@class='key-value-blocks__value']")
        sugars, fibre, protein, salt = uh[0].text, uh[1].text, uh[2].text, uh[3].text
    except:
        kcal, fat, saturates, carbs = '-','-','-','-'
        sugars, fibre, protein, salt = '-','-','-','-'
    
    return kcal, fat, saturates, carbs, sugars, fibre, protein, salt

def get_title():
    try:
        title = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "headline post-header__title post-header__title--masthead-layout")]/h1[contains(@class, "heading-1")]'))).text 
    except:
        title = '-'
    return title

def get_description():
    try:
        des = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "editor-content") and contains(@class, "post-header__description")]//p'))
    )
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
        ul_elements = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//section[@class="recipe__ingredients col-12 mt-md col-lg-6"]'))
    )
        li_elements = ul_elements.find_elements(By.TAG_NAME, 'li')
        ingredients = [li.text for li in li_elements]
        all_ingredients.extend(ingredients) 
    except:
        pass
    return all_ingredients

def get_steps():
    all_steps = []
    try:
        ul = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//section[@class="recipe__method-steps mb-lg col-12"]'))
    )
        li_elements = ul.find_elements(By.TAG_NAME, 'li')
        for li in li_elements:
            step = li.find_element(By.TAG_NAME, 'p').get_attribute('innerHTML')
            soup = BeautifulSoup(step, 'html.parser')
            step = soup.get_text(separator=' ', strip=True)  
            all_steps.append(step) 
    except:
        pass
    return all_steps

def get_metadata():
    try:
        prep_time = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "body-copy-small list-item")][1]//time'))).text
    except:
        prep_time = "-"
    try:
        cook_time = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//li[contains(@class, "body-copy-small list-item")][2]//time'))).text
    except:
        cook_time = "-"
    try:       
        serves = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//li[@class="mt-sm list-item"]//div[@class="icon-with-text__children"]'))) 
        serve = serves.get_attribute('innerHTML')
    except: 
        serve = "-"
    return prep_time, cook_time, serve

def get_image_url():
    try:
        image_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="post-header__image-container"]')))
        img = image_element.find_element(By.TAG_NAME, 'img')
        return img.get_attribute("src")
    except:
        return None
    
def get_rating():
    try:
        rating = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@class="rating__values"]//span[@class="rating__count-text body-copy-small"]'))).text
    except:
        rating = '-'
    return rating

def get_content():
    with open('finalrecipe.txt', 'r') as file:
        # for _ in range(3464):
        #     file.readline()
        for line in file:
            flag=True
            count = 0
            while flag and count<3:
                try:
                    driver.get(line.strip())
                    title = get_title()
                    if title == '-':
                        flag = True
                        count += 1
                        print(f"Retrying... Count: {count}")
                        continue
                    else:
                        flag=False
                    desc = get_description()
                    preptime, cooktime, serves = get_metadata()
                    ingrd = get_ingredients()
                    steps = get_steps()
                    imageurl = get_image_url()
                    recipeurl = driver.current_url
                    rating = get_rating()
                    kcal, fat, saturates, carbs, sugars, fibre, protein, salt = get_nutrients()
                    print(title)
                    flag=False
                    store_output(title, desc, "", rating, ingrd, serves, preptime, cooktime, steps, recipeurl, imageurl, kcal, fat, saturates, carbs, sugars, fibre, protein, salt)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    count += 1
                     
def store_output(title, desc, cuisine, rating, ingrd, serves, preptime, cooktime, steps, recipeurl, imageurl, kcal, fat, saturates, carbs, sugars, fibre, protein, salt):
    filename = "bbcgoodfood.csv"
    data=[title, desc, cuisine, rating, ingrd, serves, preptime, cooktime, "BBC Food", steps, recipeurl, imageurl, kcal, fat, saturates, carbs, sugars, fibre, protein, salt]
    with open(filename, mode="a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def load():
    while True:
        try:
            # Scroll and click the button with retry logic for stale elements
            retries = 3  # number of retry attempts for stale elements
            while retries > 0:
                try:
                    load_next_button = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'load-more-paginator__btn')]"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", load_next_button)
                    driver.execute_script("arguments[0].click();", load_next_button)  # JavaScript click
                    print("Clicked 'Load next' button")
                    break  # exit retry loop if successful
                except StaleElementReferenceException:
                    print("Stale element, retrying...")
                    retries -= 1
                    if retries == 0:
                        print("Failed after retrying for stale element")
                        break  # stop retrying after a certain number of attempts
            if retries == 0:
                break  # Exit the loop if retries are exhausted
            
        except (TimeoutException, NoSuchElementException):
            print("No more 'Load next' buttons or an error occurred.")
            break

get_content()
driver.quit()