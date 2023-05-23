import os
import time
import uuid
import json

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from seleniumbase import MasterQA

Base = declarative_base()
class ExtractedData(Base):
    __tablename__ = 'extracted_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bl_local_number = Column(String)
    business_name_english = Column(String)
    legal_type = Column(String)
    est_date = Column(String)
    ba_desc_english = Column(String)
    economic_department = Column(String)
    mobile_no = Column(String)
    phone_no = Column(String)
    email = Column(String)
    status = Column(String)
    full_address = Column(String)
    folder_path = Column(String)
    session_id = Column(String)
    extraction_status = Column(String)

class DataScrapingClass(MasterQA):
    """This class contains the methods for scraping data from the NER website."""

    def setUp(self):
        """This method runs before each test."""
        super(DataScrapingClass, self).setUp()
        self.session_id = uuid.uuid4().hex
        self.subfolder_path = os.path.join("raw_data", self.session_id)
        os.makedirs(self.subfolder_path, exist_ok=True)

        engine = create_engine('sqlite:///my_database.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        # read the json file from the raw_data folder
        self.extraction_cache = json.load(open("extraction_cache.json", "r", encoding="utf-8"))

    def tearDown(self):
        """This method runs after each test."""
        self.sleep(1)
        self.session.close()
        super(DataScrapingClass, self).tearDown()

    def test_scrape_data_from_ner_economy_ae(self):
        """This method scrapes data from the NER website."""
        while True:
            try: 
                # load the browser
                self.open("https://ner.economy.ae/Search_By_BN.aspx")

                # click the English version
                language_button_xpath = "#ctl00_SwitchLanguageButton"
                if self.get_text(language_button_xpath) == "English":
                    self.click(language_button_xpath)

                # type the name to search
                self.type("#ctl00_MainContent_View_ucSearch_By_BN_cbpBreadCrumbOverAll_BAs_txtBNEnglish", "AA")

                # wait for user to complete the captcha
                self.verify("Please enter the business name and complete the captcha manually./n You have 10 seconds to complete the task.", )
                self.sleep(8)

                # user confirms, then click the inquiry button
                self.click("#ctl00_MainContent_View_ucSearch_By_BN_cbpBreadCrumbOverAll_BAs_btnSearchButton")

                # wait for some time for the page to load
                self.sleep(5)

                # load the HTML table to a .HTML file
                while True:
                    # click on the details link for each row in the table_html
                    rows = self.find_elements("#ctl00_MainContent_View_ucSearch_By_BN_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_DXMainTable > tbody > tr")
                    rows = rows[2:]  # remove the header row and search criteria row
                    
                    if len(rows) > 0:
                        for i, row in enumerate(rows):
                            record = ExtractedData()

                            record.folder_path = self.subfolder_path
                            record.session_id = self.session_id
                            record.extraction_status = "EXTRACTION_STARTED"
                            
                            record.bl_local_number = self.get_text(f"#ctl00_MainContent_View_ucSearch_By_BN_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_DXMainTable > tbody > tr:nth-child({str(i + 3)}) > td:nth-child(1)")
                            record.business_name_english = self.get_text(f"#ctl00_MainContent_View_ucSearch_By_BN_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_DXMainTable > tbody > tr:nth-child({str(i + 3)}) > td:nth-child(3)")
                            record.status  = self.get_text(f"#ctl00_MainContent_View_ucSearch_By_BN_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_DXMainTable > tbody > tr:nth-child({str(i + 3)}) > td:nth-child(6)")
                            record.extraction_status = "PARTIAL_EXTRACTED"

                            disabled = self.get_attribute(f"#ctl00_MainContent_View_ucSearch_By_BN_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_DXMainTable > tbody > tr:nth-child({str(i + 3)}) > td > a", "class") != "aspNetDisabled"
                            if disabled:
                                self.find_element(f"#ctl00_MainContent_View_ucSearch_By_BN_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_DXMainTable > tbody > tr:nth-child({str(i + 3)}) > td > a").click()
                                
                                # wait for some time for the page to load
                                self.sleep(10)

                                record.bl_local_number = self.get_attribute('input[name="ctl00$MainContent$View_ucSearch_By_BN$popupBL_Detail$callbackPanel_BL_Detail$pop_LocalBLNo_Value"]', "value")
                                record.business_name_english = self.get_attribute('input[name="ctl00$MainContent$View_ucSearch_By_BN$popupBL_Detail$callbackPanel_BL_Detail$pop_BNEnglish_Value"]', "value")
                                record.legal_type = self.get_attribute('input[name="ctl00$MainContent$View_ucSearch_By_BN$popupBL_Detail$callbackPanel_BL_Detail$pop_LegalType_Ar_Value"]', "value")
                                record.est_date = self.get_attribute('input[name="ctl00$MainContent$View_ucSearch_By_BN$popupBL_Detail$callbackPanel_BL_Detail$pop_BLEstDate_Value"]', "value")
                                record.ba_desc_english = self.get_text('textarea[name="ctl00$MainContent$View_ucSearch_By_BN$popupBL_Detail$callbackPanel_BL_Detail$pop_BAEnglish_ISIC_Value"]')
                                record.economic_department = self.get_attribute('input[name="ctl00$MainContent$View_ucSearch_By_BN$popupBL_Detail$callbackPanel_BL_Detail$pop_Emirate_Value"]', "value")
                                record.mobile_no = self.get_attribute('input[name="ctl00$MainContent$View_ucSearch_By_BN$popupBL_Detail$callbackPanel_BL_Detail$pop_BLMobileNo_Value"]', "value")
                                record.phone_no = self.get_attribute('input[name="ctl00$MainContent$View_ucSearch_By_BN$popupBL_Detail$callbackPanel_BL_Detail$pop_BLPhoneNo_Value"]', "value")
                                record.email = self.get_attribute('input[name="ctl00$MainContent$View_ucSearch_By_BN$popupBL_Detail$callbackPanel_BL_Detail$pop_BLEmail_Value"]', "value")
                                record.status = self.get_attribute('input[name="ctl00$MainContent$View_ucSearch_By_BN$popupBL_Detail$callbackPanel_BL_Detail$pop_BLStatus_Value"]', "value")
                                record.full_address = self.get_attribute('input[name="ctl00$MainContent$View_ucSearch_By_BN$popupBL_Detail$callbackPanel_BL_Detail$pop_BLFullAddress_Value"]', "value")
                                record.extraction_status = "EXTRACTION_COMPLETED"
                                
                                # close the popup
                                self.click("#ctl00_MainContent_View_ucSearch_By_BN_popupBL_Detail_HCB-1Img")
                                self.sleep(5)
                            
                            self.session.add(record)
                            self.session.commit()
                        
                        self.extraction_cache["last_update"] = time.strftime("%Y-%m-%d %H:%M:%S")
                        self.extraction_cache["last_used_search_term"] = "AA"
                        self.extraction_cache["last_searched_page"] = int(self.extraction_cache["last_searched_page"]) + 1

                        with open("extraction_cache.json", "w", encoding="utf-8") as f:
                            json.dump(self.extraction_cache, f, indent=4)

                    # click the next page button
                    next_page_button_xpath = "#ctl00_MainContent_View_ucSearch_By_BN_cbpBreadCrumbOverAll_BAs_GeneralSearchGridView_DXPagerBottom > tbody > tr > td > table > tbody > tr > .dxpButton > .dxWeb_pPrev"
                    if self.is_element_clickable(next_page_button_xpath):
                        self.click(next_page_button_xpath)
                        self.sleep(5)

            except Exception as e:
                print(e)
                self.sleep(10)
                continue    