from selenium import webdriver
import bs4

value = input("Izberi ekipo: ")


browser = webdriver.Firefox()
browser.get("https://www.flashscore.com")
elem = browser.find_element_by_css_selector(".header__buttonIcon--search")
elem.click()
searchElem = browser.find_element_by_css_selector("#search-form-query")
searchElem.send_keys(value)
