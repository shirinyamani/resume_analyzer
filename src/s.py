import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np



    


class linkedin_scrap:

    def linkedin_open_scrolldown(driver, user_job_title):

        b = []
        for i in user_job_title:
            x = i.split()
            y = '%20'.join(x)
            b.append(y)
        job_title = '%2C%20'.join(b)

        link = f"https://in.linkedin.com/jobs/search?keywords={job_title}&location=India&locationId=&geoId=102713980&f_TPR=r604800&position=1&pageNum=0"

        driver.get(link)
        driver.implicitly_wait(10)

        for i in range(0,3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            try:
                x = driver.find_element(by=By.CSS_SELECTOR, value="button[aria-label='See more jobs']").click()
                time.sleep(3)
            except:
                pass


    def company_name(driver):

        company = driver.find_elements(by=By.CSS_SELECTOR, value='h4[class="base-search-card__subtitle"]')

        company_name = []

        for i in company:
            company_name.append(i.text)

        return company_name


    def company_location(driver):
        
        location = driver.find_elements(by=By.CSS_SELECTOR, value='span[class="job-search-card__location"]')

        company_location = []

        for i in location:
            company_location.append(i.text)
        
        return company_location
    

    def job_title(driver):
                
        title = driver.find_elements(by=By.CSS_SELECTOR, value='h3[class="base-search-card__title"]')

        job_title = []
        
        for i in title:
            job_title.append(i.text)
        
        return job_title


    def job_url(driver):

        url = driver.find_elements(by=By.XPATH, value='//a[contains(@href, "/jobs/")]')
        
        url_list = [i.get_attribute('href') for i in url]
        
        job_url = []
        
        for url in url_list:
                job_url.append(url)
        
        return job_url


    def job_title_filter(x, user_job_title):

        s = [i.lower() for i in user_job_title]
        suggestion = []
        for i in s:
            suggestion.extend(i.split())

        s = x.split()
        a = [i.lower() for i in s]

        intersection = list(set(suggestion).intersection(set(a)))
        return x if len(intersection) > 1 else np.nan


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


    def data_scrap(driver, user_job_title):

        # combine the all data to single dataframe
        df = pd.DataFrame(linkedin_scrap.company_name(driver), columns=['Company Name'])
        df['Job Title'] = pd.DataFrame(linkedin_scrap.job_title(driver))
        df['Location'] = pd.DataFrame(linkedin_scrap.company_location(driver))
        df['Website URL'] = pd.DataFrame(linkedin_scrap.job_url(driver))

        # job title filter based on user input
        df['Job Title'] = df['Job Title'].apply(lambda x: linkedin_scrap.job_title_filter(x, user_job_title))
        df = df.dropna()
        df.reset_index(drop=True, inplace=True)
        df = df.iloc[:10, :]

        # make a list after filter
        website_url = df['Website URL'].tolist()

        # add job description in df
        job_description = []

        for i in range(0, len(website_url)):
            link = website_url[i]
            data = linkedin_scrap.get_description(driver, link)
            if data is not None and len(data.strip()) > 0:
                job_description.append(data)
            else:
                job_description.append('Description Not Available')

        df['Job Description'] = pd.DataFrame(job_description, columns=['Description'])
        df = df.dropna()
        df.reset_index(drop=True, inplace=True)
        return df

if __name__ == "__main__":
        user_job_title = ['Data Analyst', 'Data Scientist']

        driver = webdriver.Chrome()
        driver.maximize_window()

        linkedin_scrap.linkedin_open_scrolldown(driver, user_job_title)

        final_df = linkedin_scrap.data_scrap(driver, user_job_title)
        driver.quit()

        print(final_df)