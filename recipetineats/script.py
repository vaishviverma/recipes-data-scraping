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
filename = "RecipeTinEats.csv"

#title,description,cuisine,rating,ingredient_list,serving,prep_time,cook_time,source,steps,recipe_url,image_url

def gettime(classname):
    
    timeel = driver.find_elements(By.CLASS_NAME, classname)
    time_ = ""
    for i in range(len(timeel)):
        time_ += timeel[i].text.replace('\n', ' ')
        time_ += " "

    return time_
        
def getdata(link):
    
    title = "-"
    description = "-"
    cuisine = "-"
    rating = "-"
    ingredients = "-"
    serving = "-"
    prep_time = "-"
    cook_time = "-"
    total_time = "-"
    source = "RecipeTinEats"
    instructions = "-"
    nutrients_f = "-"
    image_url = "-"
    

    try:
        driver.get(link)
        time.sleep(0.5)
    except:
        pass
    
    try:
        ingr_el = driver.find_elements(By.CLASS_NAME, 'wprm-recipe-ingredient')
        ingredients = [''.join(i for i in item.text if i != '▢' and i != '\n') for item in ingr_el]
        # print(ingredients)
    except:
        ingredients = "-"
    
    try:
        instr_el = driver.find_elements(By.CLASS_NAME, 'wprm-recipe-instructions')
        for item in instr_el:
            try:
                instr_els = item.find_elements(By.TAG_NAME, 'li')
                try:
                    instructions = [i.text for i in instr_els]
                except:
                    instructions = "-"
                # print(instructions)
            except:
                instructions = "-"
    except:
        instructions = "-"
    
    try:
        title = driver.find_element(By.CLASS_NAME, 'wprm-recipe-name').text
    except:
        title = "-"
    # print(title)
    
    try:
        cook_time = gettime('wprm-recipe-cook_time')
    except:
        cook_time = "-"
    try:
        prep_time = gettime('wprm-recipe-prep_time')
    except:
        prep_time = "-"
    try:
        total_time = gettime('wprm-recipe-total_time')
    except:
        total_time = "-"
        
    try:
        rating = driver.find_element(By.CLASS_NAME, 'wprm-recipe-rating-details').text
    except:
        rating = "-"
    
    try:
        cuisine = driver.find_element(By.CLASS_NAME, 'wprm-recipe-cuisine').text
    except:
        cuisine = "-"
        
    try:
        description = driver.find_element(By.CLASS_NAME, 'wprm-recipe-summary').text
        description = description.replace('\n', ' ')

        
    except:
        description = "-"
    
    try:
        serving = driver.find_element(By.CLASS_NAME, 'wprm-recipe-servings-with-unit').text
    except:
        serving = "-"
        
    source = 'RecipeTinEats'
    
    try:
        image_el = driver.find_element(By.TAG_NAME, 'img')
        image_url = image_el.get_attribute("src")   
    except:
        image_url = "-"
    
    try:
        nutrients = driver.find_element(By.CLASS_NAME, 'wprm-entry-nutrition').text

        nutrients = nutrients.split(')')
        
        nutrients = [i + ')' if i.endswith('%') else i for i in nutrients]
        
        nutrients_f = []
        for line in nutrients:
            arr = line.split(': ')
            if (len(arr) != 2):
                continue
            nutrient, value = arr[0], arr[1]
            nutrient = nutrient.split('\n')[-1]
            nutrients_f.append([nutrient, value])
    except:
        nutrients_f = "-"
        
    data = [title, description, cuisine, rating, ingredients, serving, prep_time, cook_time, total_time, source, instructions, nutrients_f, link, image_url]
    
    # print(data)
    #writing to csv
    with open(filename, mode="a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    

with open(filename, mode="w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["title","description","cuisine","rating","ingredient_list","serving","prep_time","cook_time","total_time", "source","steps", "nutrients", "recipe_url","image_url"])

links = open('recipetineats/links.txt', 'r')

for link in links:
    getdata(link)