import user
from user import *
import selenium as se
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import warnings

warnings.filterwarnings('ignore')



class Scrapper:
    def __inint__():
        pass
    
    def link(final_title):
        link = f"https://www.linkedin.com/jobs/search/?currentJobId=3805534201&geoId=101174742&keywords={final_title}&location=Canada"
        return link 
    
    
    def open_browser_and_navigate(link):
        window = input('which is your browser? Chrome/Safari')
        if window.lower() == 'chrome':
            driver  = webdriver.Chrome()
        elif window.lower() == 'safari':
            driver = webdriver.Safari()   
        else:
            raise ValueError('Unsupported browser!')
        driver.maximize_window()
        driver.get(link)
        driver.implicitly_wait(10)  
        for _ in range(0,2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
        try:
            driver.find_element(by=By.CSS_SELECTOR, value="button[aria-label='See more jobs']").click()
            time.sleep(3)
        except:
            pass 
    
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

