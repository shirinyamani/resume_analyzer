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
    
    @staticmethod
    def job_title_filter(x, user_job_title):

        s = [i.lower() for i in user_job_title]
        suggestion = []
        for i in s:
            suggestion.extend(i.split())

        s = x.split()
        a = [i.lower() for i in s]

        intersection = list(set(suggestion).intersection(set(a)))
        return x if len(intersection) > 1 else np.nan

    @staticmethod
    def get_description(driver, link):

        driver.get(link)
        time.sleep(3)

        driver.find_element(by=By.CSS_SELECTOR, 
                            value='button[data-tracking-control-name="public_jobs_show-more-html-btn"]').click()
        time.sleep(2)

        description = driver.find_elements(by=By.CSS_SELECTOR, 
                                           value='div[class="show-more-less-html__markup relative overflow-hidden"]')
        driver.implicitly_wait(4)
        
        for j in description:
            return j.text

    @staticmethod
    def data_scrap(driver, user_job_title):

        # combine the all data to single dataframe
        df = pd.DataFrame(Scrapper.company_name(driver), columns=['Company Name'])
        df['Job Title'] = pd.DataFrame(Scrapper.job_title(driver))
        df['Location'] = pd.DataFrame(Scrapper.company_location(driver))
        df['Website URL'] = pd.DataFrame(Scrapper.job_url(driver))

        # job title filter based on user input
        df['Job Title'] = df['Job Title'].apply(lambda x: Scrapper.job_title_filter(x, user_job_title))
        df = df.dropna()
        df.reset_index(drop=True, inplace=True)
        df = df.iloc[:10, :]

        # make a list after filter
        website_url = df['Website URL'].tolist()

        # add job description in df
        job_description = []

        for i in range(0, len(website_url)):
            link = website_url[i]
            data = Scrapper.get_description(driver, link)
            if data is not None and len(data.strip()) > 0:
                job_description.append(data)
            else:
                job_description.append('Description Not Available')

        df['Job Description'] = pd.DataFrame(job_description, columns=['Description'])
        df = df.dropna()
        df.reset_index(drop=True, inplace=True)
        return df








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

