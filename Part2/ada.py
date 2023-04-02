from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = ''

driver = webdriver.Chrome()

def testKeyboardNavigation(self):
  driver.get(url)
  zip_input = driver.find_element_by_id('zip_button')
  zip_input.send_keys(Keys.TAB)
  assert(driver.switch_to.active_element, zip_input, "Button test failed")
  driver.quit()