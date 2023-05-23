# Scraping

- Run a Python script using SeleniumBase to open a browser and navigate to the target website.
- Scrape the HTML of the page and save it in a dynamically created subfolder under the raw_data/ directory. The subfolder should be named based on a unique execution ID.
- Store the HTML data in .html files, each named according to a unique record ID.
- Keep track of the folder paths, execution ID, record ID, and extraction status in an Excel file under the raw_data/ directory. The extraction status for each record is set to "SCRAPING_DONE".

# Processing

- Run a second Python script which reads the Excel file under the raw_data/ directory.
- Parse the HTML files corresponding to records where the status is "SCRAPING_DONE" using BeautifulSoup.
- Extract required data based on a predefined dictionary containing XPath values.
- Save the extracted data in an Excel file under the processed_data/ directory. The file should be named based on the execution ID, date, time, and a hard-coded string "transformed".
- The processed data Excel file should also contain the corresponding record ID from the raw data Excel file.
- Update the status in the raw data Excel file to "TRANSFORMED" for each processed record.

# Loading

- Run a final script named "load_data".
- Compile all the transformed Excel files in the processed_data/ directory into a single dataset.
- Remove duplicate entries based on a specific field.
- Check for missing mandatory fields in each record and remove any records where these are missing.
- Update the status in the raw data Excel file to "LOADED" for each loaded record.