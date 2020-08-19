from selenium import webdriver
import bs4
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

value = "Barcelona"

#Creates a browser and visits flashscore webpace
browser = webdriver.Firefox()
browser.get("https://www.flashscore.com/")

#Identifies search button, searches for desired team, heads to team page
search_button = browser.find_element_by_css_selector(".header__buttonIcon--search")
search_button.click()
search_bar = browser.find_element_by_css_selector("#search-form-query")
search_bar.send_keys(value)
browser.implicitly_wait(1)
result_element = browser.find_element_by_css_selector("#search-results > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > a:nth-child(1)")
result_element.click()

#Extracts game id's into a list
games = browser.find_elements_by_class_name("event__match")
game_ids = []
for game in games:
    game_ids.append(game.get_attribute("id"))





