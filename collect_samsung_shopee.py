from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire.utils import decode
from selenium.webdriver.support.ui import WebDriverWait
import time
import json

driver = webdriver.Chrome()
# search samsung with handphone category
# url = "https://shopee.co.id/search?facet=11044476&keyword=samsung&noCorrection=true&page=0"
url = "https://shopee.co.id/search?facet=11044476&keyword=samsung&noCorrection=true&order=desc&page=0&sortBy=price" 
driver.get(url)
all_data = []
urls_listed = []

def is_hit(url):
    for i in urls_listed:
        if i == url:
            return True
    urls_listed.append(url)
    return False
    
try:
    # first page
    # find search result element class
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "(//div[@class='shopee-search-item-result'])[1]")))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")   
    # intercept API request 
    for request in driver.requests:
        if "search_items" in request.url:
            if is_hit(request.url) != True and request.response:
                tmp = json.loads(decode(request.response.body, request.response.headers.get("Content-Encoding", "identity")))
                all_data.extend(tmp["items"])
                
    time.sleep(5)
    total_page = driver.find_element(By.XPATH, "//span[@class='shopee-mini-page-controller__total']")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("Total pages: ", total_page.text)
    
    # next page until total_page
    for i in range(1, int(total_page.text) + 1):
        print("Current Page: ", i )
        
        try:
            # find search result element class
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "(//div[@class='shopee-search-item-result'])[1]")))
            next_btn = driver.find_element(By.XPATH, "//button[@class='shopee-button-outline shopee-mini-page-controller__next-btn']")
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.execute_script("arguments[0].click();", next_btn)
            
            for request in driver.requests:
                if "search_items" in request.url:
                    if is_hit(request.url) != True and request.response:
                        tmp = json.loads(decode(request.response.body, request.response.headers.get("Content-Encoding", "identity")))
                        all_data.extend(tmp["items"])
                        print(request.url)
            time.sleep(10)    
           
        except Exception as e:
            print("Error ", e)
      

finally:
    save_file = open("samsung-shopee.json", "w")  
    json.dump(all_data, save_file, indent = 4)  
    save_file.close()  
    driver.close()