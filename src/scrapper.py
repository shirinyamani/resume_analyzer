from user import User
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
        company = driver.find_elements(by=By.CSS_SELECTOR, value='h4[class="base-search-card__subtitle"]')
        company_name = []
        for i in company:
            company_name.append(i.text)
        return company_name
    
    @staticmethod
    def company_location(driver):
        location = driver.find_elements(by=By.CSS_SELECTOR, value='span[class="job-search-card__location"]')
        company_location = []
        for i in location:
            company_location.append(i.text)
        return company_location

    @staticmethod
    def job_title(driver):
        title = driver.find_elements(by=By.CSS_SELECTOR, value='h3[class="base-search-card__title"]')
        job_title = []
        for i in title:
            job_title.append(i.text)
        return job_title

    @staticmethod
    def job_url(driver):
        url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
        url_list = [i.get_attribute('href') for i in url]
        job_url = []
        for url in url_list:
                job_url.append(url)
        return job_url

        
    @staticmethod
    def df_jobs_data(driver):
        company_name = Scrapper.company_name(driver)

        company_location = Scrapper.company_location(driver)
      
        job_title = Scrapper.job_title(driver)
    
        job_url = Scrapper.job_url(driver)
      
        min_length = min(len(company_name), len(company_location), len(job_title), len(job_url))
        index = range(1, min_length + 1)
        jobs_data = pd.DataFrame(
            {'Company Name': company_name,
            'Company Location': company_location,
            'Job Title': job_title,
            'Job URL': job_url
            }, index=index)
        # Use range to create an index of the same length
        

        print(jobs_data)
        return jobs_data
        
        


if __name__ == "__main__":
    user = User()

    job_list = user.ask_job_keyword()

    if User.verify_jobs():
        final_title = user.convert_to_right(job_list)
        search_link = user.link(final_title)

        # Create the WebDriver instance outside the class
        driver = webdriver.Chrome()

        # Now let's use the Scrapper class
        scrapper = Scrapper()
        scrapper.open_browser_and_navigate(driver, search_link)

        # Get all jobs data
        all_jobs_data = scrapper.df_jobs_data(driver)
        print(all_jobs_data)

        # Close the browser window when done
        driver.quit()
    else:
        print('Please enter the job keywords again.')
