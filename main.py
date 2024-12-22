from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time

def execute_search_query(driver, search_query):
     # get search box
     search_box = driver.find_element(value = 'APjFqb')
     # insert search query
     search_box.send_keys(search_query)
     # execute the search
     search_box.send_keys(Keys.RETURN)


def find_description(dom_result):
     # known possible css selectors for the div in where the description is
     selectors = ['[data-sncf="1"]', '[data-sncf="1,2"]']
     for selector in selectors:
          try:
               descriptionDiv = dom_result.find_element(By.CSS_SELECTOR, value = selector)
               return descriptionDiv.get_attribute("innerText")
          except:
               print('description selector failed, trying another one')
     return 'None'


def scrape_search_results(url):
     # init the WebDriver
     driver = webdriver.Chrome()
     try:
          # open google in web browser and search query
          driver.get(url)
          execute_search_query(driver, 'hello world')
          # wait for the results to load
          time.sleep(5)
          # extract the first 10 results 
          # (each page has 10 regular results and some other so we take 20 and filter later on)
          results = driver.find_elements(By.CSS_SELECTOR ,value = 'div.g')[:20]
          data = []
          for idx, result in enumerate(results):
               # get elements
               title = result.find_element(By.TAG_NAME, value = 'h3').text
               description = find_description(result)
               url = result.find_element(By.TAG_NAME, value = 'a').get_attribute('href')
               # filter incomplete results that may come from the 'People also asked' section
               if title != "" and description != "":
                    data.append({"Title": title, "Description": description, "URL": url})
                    print(f'scraped result no {idx + 1}: {title}')

          # Save the extracted data into an Excel file
          df = pd.DataFrame(data)
          df.to_excel("search_results.xlsx", index=False)
     except: 
          print('critical driver fail, cannot scrape results')
     finally:
          # Close the WebDriver
          driver.quit()
          print('scraping finished, driver terminated gracefully')

scrape_search_results("https://www.google.com")
