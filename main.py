# main.py
#
from src import DataScrapingClass, process_raw_data

if __name__ == "__main__":
    # instantiate the DataScrapingClass
    scraper = DataScrapingClass()
    scraper.scrape_data_from_ner_economy_ae()
