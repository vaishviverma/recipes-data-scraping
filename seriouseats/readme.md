Note: Before running any script, you must properly download the chromedriver folder, depending on your OS. After this, replace the path in each script with the path of your chromedriver. To find where to replace, simply search "chromedriver".

This has 3 files:

extractLinks.py - This extracts direct links to recipes by opening different categories (links to which had to be hardcoded, no better way).

extractLinksCuisines.py - This extracts direct links to recipes having cuisine. Again, we're opening cuisine based categories on the website, links to which have been hardcoded.

The above two files store links in different files. Entirely copy "cuisine_links.txt" (created when the extractLinksCuisine.py was run) and paste it at the BOTTOM of "links.txt" (created when the extractLinks.py was run).

Finally, run extract.py and watch magic happen.
