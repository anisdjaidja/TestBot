from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

# init the WebDriver
driver = webdriver.Chrome()
try:
     # open google in web browser and search query
     driver.get("https://www.google.com")
     execute_search_query(driver, 'hello world')
     time.sleep(2)
     results = driver.find_elements_by_css_selector('div.g')[:10]
     data = []
     for result in results:
          title = result.find_element_by_tag_name('h3').text
          description = find_description(result)
          url = result.find_element_by_tag_name('a').get_attribute('href')
          data.append({"Title": title, "Description": description, "URL": url})
     df = pd.DataFrame(data)
     df.to_excel("search_results.xlsx", index=False)

finally:
     driver.quit()
