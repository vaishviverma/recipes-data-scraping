from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv

# function to set up and return the selenium webdriver
def setup(driver_path):
    # configure the chrome driver service
    chrome_service = Service(executable_path=driver_path)
    # set up chrome options to customize browser behavior
    chrome_options = Options()
    # disable popup blocking to ensure smooth navigation
    chrome_options.add_argument("--disable-popup-blocking")
    # return the configured webdriver
    return webdriver.Chrome(service=chrome_service, options=chrome_options)

# initialize the selenium webdriver with the specified driver path
driver = setup('chromedriver-linux64/chromedriver')

# list of urls representing different cuisine categories
bases = [
    "https://www.seriouseats.com/african-recipes-5117276",
    "https://www.seriouseats.com/asian-recipes-5117262",
    "https://www.seriouseats.com/caribbean-recipes-5117182",
    "https://www.seriouseats.com/central-american-recipes-5117207",
    "https://www.seriouseats.com/europe-recipes-5117236",
    "https://www.seriouseats.com/middle-eastern-recipes-5117255",
    "https://www.seriouseats.com/north-american-recipes-5117205",
    "https://www.seriouseats.com/oceanic-recipes-5117211",
    "https://www.seriouseats.com/south-american-recipes-5117188",
    "https://www.seriouseats.com/world-cuisine-guides-5117177",
    "https://www.seriouseats.com/southern-european-recipes-5117225",
    "https://www.seriouseats.com/eastern-european-recipes-5117235",
    "https://www.seriouseats.com/northern-european-recipes-5117230",
    "https://www.seriouseats.com/western-european-recipes-5117217",
    "https://www.seriouseats.com/thai-recipes-5117239",
    "https://www.seriouseats.com/cambodian-recipes-5117244",
    "https://www.seriouseats.com/filipino-recipes-5117243",
    "https://www.seriouseats.com/indonesian-recipes-5117242",
    "https://www.seriouseats.com/laotian-recipes-5117241",
    "https://www.seriouseats.com/malaysian-recipes-5117240",
    "https://www.seriouseats.com/singaporean-recipes-5117238",
    "https://www.seriouseats.com/vietnamese-recipes-5117237",
    "https://www.seriouseats.com/asian-recipes-5117262",
    "https://www.seriouseats.com/central-asian-cuisine-guides-5117163",
    "https://www.seriouseats.com/east-asian-cuisine-guides-5117162",
    "https://www.seriouseats.com/south-asian-cuisine-guides-5117153",
    "https://www.seriouseats.com/middle-eastern-cuisine-guides-5117157"
]

# iterate through each base url in the list
for link in bases:
    # extract the cuisine name from the url for labeling
    arr = link.split("/")
    cuisine_name = ""
    for i in arr[3].split("-"):
        cuisine_name += i
        cuisine_name += " "
    # remove the trailing space from the cuisine name
    cuisine_name = cuisine_name[:-1]
    
    # open a file in append mode to store links
    with open("cuisine_links", "a") as file:
        # load the base url in the browser
        driver.get(link)
        # wait for the page to fully load
        time.sleep(1)
        # find all elements with the specified class name
        links = driver.find_elements(By.CLASS_NAME, 'mntl-document-card')
        # write the cuisine name as a header
        file.write("#" + cuisine_name + "\n")
        # iterate through each link and write its href attribute to the file
        for i in links:
            file.write(i.get_attribute("href") + "\n")
