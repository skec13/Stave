
from selenium import webdriver
import bs4
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import requests
import time

value = "Barcelona"

#Creates a browser and visits flashscore webpace
browser = webdriver.Firefox()
browser.get("https://www.flashscore.com/")

#Identifies search button, searches for desired team, heads to team page
search_button = browser.find_element_by_css_selector(".header__buttonIcon--search")
search_button.click()
search_bar = browser.find_element_by_css_selector("#search-form-query")
search_bar.send_keys(value)
browser.implicitly_wait(2)
result_element = browser.find_element_by_css_selector("#search-results > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > a:nth-child(1)")
result_element.click()

#Shows more matches
show_matches = browser.find_element_by_css_selector(".event__more")
show_matches.click()
browser.implicitly_wait(2) #wait for 2 secords(maybe 1 second is enough??)
show_matches1 = browser.find_element_by_css_selector(".event__more")
show_matches1.click()

#Extracts game id's into a list of links
games = browser.find_elements_by_class_name("event__match")
game_links = []
for game in games:
    game_id = game.get_attribute("id")
    game_links.append("https://www.flashscore.com/match/" + game_id[4:] + "/#match-statistics;0")

#Visits every game stats site and scraps data into lists
huge_list = []
for page in game_links:
    browser.get(page)
    element = browser.find_elements_by_class_name("statTextGroup")  #Unnecessary?
    soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
    tag = soup.find_all('div', {"class": "statTextGroup"})
    medium_list = []
    for el in tag:
        stat = []
        mini_list = el.find_all('div')
        for el in mini_list:
            stat.append(el.text)
        medium_list.append(stat)
    huge_list.append(medium_list)

browser.quit()

