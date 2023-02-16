from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By

from time import sleep

# Create your tests here.
def test():
    driver = webdriver.Firefox()
    driver.get('http://127.0.0.1:8000/')
    driver.implicitly_wait(1000)
    driver.find_element(By.NAME, "findby").submit()
    sleep(1)
    driver.find_element(By.CLASS_NAME, 'Login').click()
    sleep(1)

    driver.find_element(By.NAME, 'login').send_keys('userHash')
    sleep(1)
    driver.find_element(By.NAME, 'password').send_keys('12345678')
    sleep(1)
    driver.find_element(By.NAME, 'login').submit()
    sleep(1)
    driver.find_element(By.NAME, "findby").submit()
    sleep(1)
    add_manga = driver.find_elements(By.NAME, "addtocart")
    add_manga[0].click()
    sleep(1)
    driver.find_element(By.NAME, "add").submit()
    driver.find_element(By.NAME, "findby").submit()
    sleep(1)
    add_manga = driver.find_elements(By.NAME, "addtocart")
    add_manga[1].click()
    sleep(1)
    driver.find_element(By.NAME, "add").submit()
    driver.find_element(By.NAME, "findby").submit()
    sleep(1)
    driver.find_element(By.CLASS_NAME, 'cart').click()
    sleep(1)
    driver.find_element(By.NAME, 'create').click()
    sleep(1)
    driver.find_element(By.NAME, 'name').send_keys('userHash')
    sleep(1)
    driver.find_element(By.NAME, "create").submit()
    sleep(1)
    driver.find_element(By.NAME, "findby").submit()
    sleep(1)
    driver.find_element(By.CLASS_NAME, "allOrders").click()
    sleep(1)
    driver.find_element(By.CLASS_NAME, 'main').click()
    driver.find_element(By.NAME, "findby").submit()
    sleep(2)
    print('OK')
    driver.find_element(By.CLASS_NAME, 'user_logout').click()
    driver.find_element(By.NAME, "findby").submit()
    sleep(1)



    

if __name__ == "__main__":
    test()
