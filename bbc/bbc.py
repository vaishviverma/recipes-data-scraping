# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import csv
import re
import string



# Creating a 'bbc.csv' file to store recipe information
filename = "bbc.csv"
with open(filename, mode="w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)

    # Parameters for each recipe: recipe_title, description, cuisine, rating, ingredient_list, servings, 
    #                             prep_time, cook_time, total_time, source, steps, recipe_url, image_url

    writer.writerow(["title","description","cuisine","rating","ingredient_list",
                     "serving","prep_time","cook_time","source","steps","recipe_url","image_url"])

# Define paths and initialize the Chrome WebDriver
driver_path = 'chromedriver-win32\chromedriver.exe'
website = 'https://www.bbc.co.uk/food/cuisines'
chrome_service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=chrome_service)


# List of Cuisines available on the website
cuisine_list = ["british","african","american","italian","indian","caribbean","chinese","east_european","french","greek","irish","japanese","korean","mexican",
           "nordic","pakistani","north_african","portuguese","south-american","spanish","turkish_and_middle_eastern","thai_and_south-east_asian"]


# List that will store links of recipes from different cuisines in the form [recipe_link, Cuisine] for each recipe link.
links=[]

# Function to extract recipe title
def get_title():
    try:
        title_element = driver.find_element(By.XPATH, "//h1[@class='gel-trafalgar content-title__text']").text
    except:
        title_element = '-'
    return title_element


# Function to extract recipe description
def get_description():
    try:
        des = driver.find_element(By.XPATH, "//p[@class='recipe-description__text']")
        inner_html = des.get_attribute('innerHTML')
        desc = re.sub(r'<br\s*\/?>', ' ', inner_html) # Replace <br> tags with spaces
        desc = re.sub(r'<.*?>', '', desc) # Remove other HTML tags
        desc = " ".join(desc.split()) # Clean up extra whitespace
    except: 
        desc = "-"
    return desc


# Function to extract the list of ingredients
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


# Function to extract list of steps
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


# Function to extract metadata like prep time, cook time, and servings
def get_metadata():
    try:
        prep_time = driver.find_elements(By.XPATH, "//p[@class='recipe-metadata__prep-time']")[-1].text
    except:
        prep_time = "-"
    try:
        cook_time = driver.find_elements(By.XPATH, "//p[@class='recipe-metadata__cook-time']")[-1].text
    except:
        cook_time = "-"
    try:        
        serves = driver.find_elements(By.XPATH, "//p[@class='recipe-metadata__serving']")[-1].text
    except: 
        serves = "-"
    return prep_time, cook_time, serves


# Function to extract image_url
def get_image_url():
    try:
        image_element = driver.find_element(By.XPATH, "//div[@class='recipe-media__image responsive-image-container__16/9']")
        img_url = image_element.find_element(By.TAG_NAME, 'img')
        return img_url.get_attribute("src")
    except:
        return None
    

#Functiont to extract rating of recipe
def get_rating():
    try:
        rating = driver.find_element(By.XPATH, "//span[contains(@class, 'aggregate-rating__total') and contains(@class, 'gel-long-primer-bold')]").text
    except:
        rating = '-'
    return rating


# Function to extract links of recipes from every cuisine in the list 'cuisine_list'
def get_recipe_links():
    for cuisine in cuisine_list:
        for letter in string.ascii_lowercase:
            try:

                # Construct URL for each cuisine
                url = "https://www.bbc.co.uk/food/cuisines/"+ cuisine +"/a-z/" + letter
                driver.get(url)
                if driver.current_url == ("https://www.bbc.co.uk/food/cuisines/"+ cuisine):
                    driver.back()
                    continue

                flag = True

                while flag==True:

                    # Extract links to recipes

                    elements = driver.find_elements(By.XPATH,"//div[@class='gel-layout__item gel-1/2 gel-1/3@m gel-1/4@xl']")
                    for el in elements:
                        links.append([el.find_element(By.TAG_NAME,'a').get_attribute("href"), cuisine])


                    # Check for and navigate to the next page
                    try:
                        next_page = driver.find_elements(By.XPATH,"//li[@class='pagination__list-item pagination__priority--0']")
                        page = next_page[-1].find_element(By.TAG_NAME,'a')
                        if page.get_attribute("href")!=driver.current_url:
                            driver.get(page.get_attribute("href"))
                    except:
                        flag=False
                    
            except:
                pass


# Function to scrape recipe data for each link
def get_recipe_data():
    # Access each link in links.txt
    with open('links.txt', 'r') as file:
        for line in file:
            link, cuisine = line.strip().split(',')
            driver.get(link)
            title = get_title()
            desc = get_description()
            preptime, cooktime, serves = get_metadata()
            ingrd = get_ingredients()
            steps = get_steps()
            imageurl = get_image_url()
            recipeurl = driver.current_url
            rating = get_rating()
            store_output(title, desc, cuisine, rating, ingrd, serves, preptime, cooktime, steps, recipeurl, imageurl)


# Function to store recipe data into the CSV
def store_output(title, desc, cuisine, rating, ingrd, serves, preptime, cooktime, steps, recipeurl, imageurl):
    filename = "bbc.csv"
    data=[title, desc, cuisine, rating, ingrd, serves, preptime, cooktime, "BBC Food", steps, recipeurl, imageurl]
    with open(filename, mode="a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)


# Function to save all links to 'links.txt' file for later use
def store_links(links):
    with open('links.txt', 'w') as file:
        for link in links:
            file.write(link[0]+","+link[1]+"\n")


get_recipe_links()  # To scrape recipe links + its cuisine and store in a list
store_links(links)  # To store the list in a links.txt file
get_recipe_data()  # To scrape recipe data from each link stored in links.txt and store in bbc.csv file

driver.quit()  # Close browser