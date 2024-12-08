from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv

# function to set up the selenium webdriver
def setup(driver_path):
    # define the service for the chrome driver
    chrome_service = Service(executable_path=driver_path)
    chrome_options = Options()
    # disable popup blocking for smooth navigation
    chrome_options.add_argument("--disable-popup-blocking")
    # return the configured webdriver
    return webdriver.Chrome(service=chrome_service, options=chrome_options)

# initialize the webdriver
driver = setup('chromedriver-linux64/chromedriver')

# list of base urls to scrape recipe links from
bases = [
    "https://www.seriouseats.com/chicken-main-recipes-5117832", 
    "https://www.seriouseats.com/fall-recipes-5117983",
    "https://www.seriouseats.com/summer-recipes-5117942",
    "https://www.seriouseats.com/vegetarian-main-recipes-5117754",
    "https://www.seriouseats.com/fat-oil-recipes-5117670",
    "https://www.seriouseats.com/pasta-main-recipes-5117817",
    "https://www.seriouseats.com/fall-main-recipes-5117978",
    "https://www.seriouseats.com/sous-vide-recipes-5117306",
    "https://www.seriouseats.com/vegetarian-recipes-5117757",
    "https://www.seriouseats.com/italian-recipes-with-chicken-8631574",
    "https://www.seriouseats.com/guide-to-chili-styles-types-of-chili-recipes",
    "https://www.seriouseats.com/pizza-recipes-5117816",
    "https://www.seriouseats.com/chicken-recipes-5117694",
    "https://www.seriouseats.com/recipes-by-ingredient-recipes-5117749",
    "https://www.seriouseats.com/quick-dinner-recipes-5117810",
    "https://www.seriouseats.com/recipes-by-diet-5117779",
    "https://www.seriouseats.com/recipes-by-course-5117906",
    "https://www.seriouseats.com/recipes-by-world-cuisine-5117277",
    "https://www.seriouseats.com/main-recipes-5117839",
    "https://www.seriouseats.com/recipes-by-method-5117399",
    "https://www.seriouseats.com/winter-main-recipes-5117911",
    "https://www.seriouseats.com/rice-grain-recipes-5117567",
    "https://www.seriouseats.com/chickpea-recipes-5117741",
    "https://www.seriouseats.com/main-recipes-by-diet-5117838", 
    "https://www.seriouseats.com/vegan-recipes-5117764", 
    "https://www.seriouseats.com/holiday-season-recipes-5117984", 
    "https://www.seriouseats.com/summer-main-recipes-5117934", 
    "https://www.seriouseats.com/mushroom-recipes-5117454", 
    "https://www.seriouseats.com/peanut-recipes-5117596", 
    "https://www.seriouseats.com/cinco-de-mayo-recipes-5117961", 
    "https://www.seriouseats.com/spring-recipes-5117963", 
    "https://www.seriouseats.com/poaching-recipes-5117331", 
    "https://www.seriouseats.com/vegetable-main-recipes-5117825", 
    "https://www.seriouseats.com/beef-recipes-5117732", 
    "https://www.seriouseats.com/cookie-recipes-5117873", 
    "https://www.seriouseats.com/stovetop-egg-recipes-5117288", 
    "https://www.seriouseats.com/egg-recipes-5117678",
    "https://www.seriouseats.com/soup-recipes-5117814", 
    "https://www.seriouseats.com/pressure-cooker-recipes-5117325", 
    "https://www.seriouseats.com/salad-recipes-5117809", 
    "https://www.seriouseats.com/south-american-recipes-5117188",
    "https://www.seriouseats.com/potato-recipes-5117428",
    "https://www.seriouseats.com/northern-european-recipes-5117230",
    "https://www.seriouseats.com/italian-recipes-5117222",
    "https://www.seriouseats.com/mexican-recipes-5117189",
    "https://www.seriouseats.com/south-american-recipes-5117188",
    "https://www.seriouseats.com/whole-chicken-recipes-5117685",
    "https://www.seriouseats.com/main-recipes-by-ingredient-5117837",
    "https://www.seriouseats.com/savory-recipes-5117375",
    "https://www.seriouseats.com/air-fryer-recipes-8549755",
    "https://www.seriouseats.com/east-asian-recipes-5117260",
    "https://www.seriouseats.com/chinese-american-recipes-5117201",
    "https://www.seriouseats.com/grilling-recipes-5117350",
    "https://www.seriouseats.com/african-recipes-5117276",
    "https://www.seriouseats.com/tomato-recipes-5117409",
    "https://www.seriouseats.com/drink-recipes-5117861",
    "https://www.seriouseats.com/chinese-recipes-5117259",
    "https://www.seriouseats.com/dessert-recipes-5117878",
    "https://www.seriouseats.com/gluten-free-recipes-5117770",
    "https://www.seriouseats.com/main-recipes-by-type-5117824"
]

# open the file in write mode to store links
with open("links.txt", "w") as file:
    # iterate through each base url
    for link in bases:
        # navigate to the url using the webdriver
        driver.get(link)
        # find all elements containing recipe links
        links = driver.find_elements(By.CLASS_NAME, 'mntl-document-card')
        # extract and write each link to the file
        for i in links:
            file.write(i.get_attribute("href") + "\n")
