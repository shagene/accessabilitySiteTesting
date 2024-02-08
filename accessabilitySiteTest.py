from selenium import webdriver
from axe_selenium_python import Axe
import pprint

driver = webdriver.Chrome()  # Replace 'Chrome' with your desired browser
driver.get('URL')

axe = Axe(driver)
axe.inject()  # Inject axe-core into the browser page

results = axe.run()
driver.quit()

pprint.pprint(results['violations'])
