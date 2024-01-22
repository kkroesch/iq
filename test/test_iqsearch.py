# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestTestiqsearch():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_testiqsearch(self):
    self.driver.get("http://localhost:8000/")
    self.driver.set_window_size(1536, 832)
    self.driver.find_element(By.NAME, "query").click()
    self.driver.find_element(By.NAME, "query").send_keys("pfahlbauten")
    self.driver.find_element(By.NAME, "query").send_keys("pfahlbauten")
    self.driver.find_element(By.NAME, "query").send_keys(Keys.ENTER)
    self.driver.find_element(By.CSS_SELECTOR, "html").click()
    self.driver.find_element(By.NAME, "query").click()
    self.driver.find_element(By.NAME, "query").send_keys("vmware")
    self.driver.find_element(By.NAME, "query").send_keys(Keys.ENTER)
  