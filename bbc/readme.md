Note: Before running any script, you must properly download the chromedriver folder, depending on your OS. After this, replace the path in each script with the path of your chromedriver. To find where to replace, simply search "chromedriver".

Single-step: Run "bbc.py". This first creates a list of recipe links, opening each cuisine page on the website.
The "store_links()" function is responsible for storing links.
Then, these links are opened one by one and recipes are scraped.