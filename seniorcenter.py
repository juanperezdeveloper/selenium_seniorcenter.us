from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver
import time

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/80.0.3987.132 Safari/537.36'

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f'user-agent={user_agent}')
options.headless = True

def get_info():
    url = 'https://seniorcenter.us/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html5lib")
    try:
        us_maps = soup.find(id='usmap').findAll('area')
    except:
        us_maps = []
    with open('output.csv','w', newline='') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        wr.writerow(['Name', 'State', 'City', 'Address', 'Phone', 'Contact Name', 'Email address', 'Website', 'Details', 'Membership Information', 'Services', 'Age requirements', 'Operation Time'])
    
    driver = webdriver.Chrome(options = options)
    driver.set_page_load_timeout(20)
    for us_map in us_maps:
        state = us_map.get('title').split('(')[0].strip()
        response = requests.get(url[:-1] + us_map.get('href'))
        try:
            soup = BeautifulSoup(response.content, "html5lib")
            city_urls = soup.find('div', attrs={'class', 'us_cities'}).findAll('a')
        except:
            city_urls = []
        for city_url in city_urls:
            city = city_url.get_text().split('(')[0].strip()
            response = requests.get(url[:-1] + city_url.get('href'))
            try:
                soup = BeautifulSoup(response.content, "html5lib")
                center_urls = soup.find('article', attrs={'class', 'city_8'}).findAll('a')
            except:
                center_urls = []
            for center_url in center_urls:
                page = ''
                while page== '':
                    try:
                        driver.get(url[:-1] + center_url.get('href'))
                        page = driver.page_source
                        try:
                            name = driver.find_element_by_xpath("//div[contains(text(),'Name')]/following-sibling::div").text
                        except:
                            name = ''
                        try:
                            address = driver.find_element_by_xpath("//div[contains(text(),'Address')]/following-sibling::div").text.replace('\n', ' ').replace(',', ' ')
                        except:
                            address = ''
                        try:
                            phone = driver.find_element_by_xpath("//div[contains(text(),'Phone')]/following-sibling::div").text.replace(',', ' ')
                        except:
                            phone = ''
                        try:
                            contact_name = driver.find_element_by_xpath("//div[contains(text(),'Contact Name')]/following-sibling::div").text.replace(',', ' ')
                        except:
                            contact_name = ''
                        try:
                            email_address = driver.find_element_by_xpath("//div[contains(text(),'Email address')]/following-sibling::div").text.replace(',', ' ')
                        except:
                            email_address = ''
                        try:
                            website = driver.find_element_by_xpath("//div[contains(text(),'Website')]/following-sibling::div").text.replace(',', ' ')
                        except:
                            website = ''
                        try:
                            details = driver.find_element_by_xpath("//div[contains(text(),'Details')]/following-sibling::div").text.replace(',', ' ')
                        except:
                            details = ''
                        try:
                            membership_information = driver.find_element_by_xpath("//div[contains(text(),'Membership Information')]/following-sibling::div").text.replace(',', ' ')
                        except:
                            membership_information = ''
                        try:
                            services = driver.find_element_by_xpath("//div[contains(text(),'Services')]/following-sibling::div").text.replace(',', ' ')
                        except:
                            services = ''
                        try:
                            age_requirements = driver.find_element_by_xpath("//div[contains(text(),'Age requirements')]/following-sibling::div").text.replace(',', ' ')
                        except:
                            age_requirements = ''
                        try:
                            operation_time = driver.find_element_by_xpath("//div[contains(text(),'Operation Time')]/following-sibling::div").text.replace(',', ' ')
                        except:
                            operation_time = ''
                        results = [name, state, city, address, phone, contact_name, email_address, website, details, membership_information, services, age_requirements, operation_time]
                        
                        if name != '':
                            with open('output.csv','a', newline='') as result_file:
                                wr = csv.writer(result_file, dialect='excel')
                                wr.writerow(results)
                    except:
                        time.sleep(3)
                        driver.quit()
                        driver = webdriver.Chrome(options = options)
                        driver.set_page_load_timeout(20)
        
if __name__ == "__main__":
    get_info()