from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

driver = webdriver.Chrome()

try:
    driver.get("https://www.google.com")
    search_box = driver.find_element_by_name("q")
    search_box.send_keys("hello world")
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    results = driver.find_elements_by_css_selector('div.g')[:10]
    data = []
    for result in results:
        title = result.find_element_by_tag_name('h3').text
        description = result.find_element_by_css_selector('span.aCOpRe').text
        url = result.find_element_by_tag_name('a').get_attribute('href')
        data.append({"Title": title, "Description": description, "URL": url})
    df = pd.DataFrame(data)
    df.to_excel("search_results.xlsx", index=False)

finally:
    driver.quit()
