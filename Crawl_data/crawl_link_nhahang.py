from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchAttributeException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

import pandas as pd
driver = webdriver.Chrome()

url = 'https://shopeefood.vn/ha-noi/food/deals'
driver.get(url)
sleep(3)

with open('links.txt', 'w', encoding='utf-8') as file:
    count = 0
    while True:
        try:
            # names = [name.text for name in driver.find_elements(By.XPATH, "//a/div[2]/div[1]/h4")]
            links = [link.get_attribute("href") for link in driver.find_elements(By.CSS_SELECTOR , ".item-content")]
            click = driver.find_element(By.CSS_SELECTOR, ".icon.icon-paging-next")
            click.click()
            sleep(2)
            for link in links:
                file.write(link + '\n')
            count += 1
            if count == 80:
                break
        except:
            print("Error")

driver.quit()
