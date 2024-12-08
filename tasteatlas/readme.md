Note: Before running any script, you must properly download the chromedriver folder, depending on your OS. After this, replace the path in each script with the path of your chromedriver. To find where to replace, simply search "chromedriver".

Firstly, we will scrape the recipes using tasteatlas.py and then we'll process the data using data_analysis.py

The post-processing makes changes to the ingredient list removing unnecessary capitalized words which are not ingredients.

Step 1: Run tasteatlas.py

Step 2: Make sure the file that has recipes is named 'tasteatlas.csv' (should be by default), and then run data_analysis.py.