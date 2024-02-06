import user
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings('ignore')

class Scrapper:

    @staticmethod
    def open_browser_and_navigate(driver, link):
        driver.maximize_window()
        driver.get(link)
        driver.implicitly_wait(10)
        for _ in range(0, 2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
        try:
            driver.find_element(by=By.CSS_SELECTOR, value="button[aria-label='See more jobs']").click()
            time.sleep(3)
        except:
            pass

    @staticmethod
    def company_name(driver):
        company = driver.find_elements(by=By.CSS_SELECTOR, value='a[class="job-search-card__subtitle-link"]')
        company_name = [i.text for i in company]
        return company_name
    
    @staticmethod
    def company_location(driver):
        location = driver.find_elements(by=By.CSS_SELECTOR, value='span[class="job-search-card__location"]')
        company_location = [i.text for i in location]
        return company_location

    @staticmethod
    def job_title(driver):
        title = driver.find_elements(by=By.CSS_SELECTOR, value='h3[class="base-search-card__title"]')
        job_title = [i.text for i in title]
        return job_title

    @staticmethod
    def job_url(driver):
        url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
        job_url = [i.get_attribute('href') for i in url]
        return job_url
    
    



if __name__ == "__main__":
    job_list = user.User.ask_job_keyword()

    if user.User.verify_jobs():
        final_title = user.User.convert_to_right(job_list)
        search_link = user.User.link(final_title)

        # Create the WebDriver instance outside the class
        driver = webdriver.Chrome()

        # Now let's use the Scrapper class
        scrapper = Scrapper()
        Scrapper.open_browser_and_navigate(driver, search_link)

        # Assuming 'driver' is the WebDriver instance you created
        results_df = Scrapper.data_scrap(driver, job_list)
        print(results_df)

        # Close the browser window when done
        driver.quit()
    else:
        print('Please enter the job keywords again.')

