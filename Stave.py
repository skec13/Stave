from selenium import webdriver
import bs4
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import requests
import time

value = "Barcelona"
value_2 = "Arsenal"

def get_match_history(team):
        
    #Creates a browser and visits flashscore webpace
    browser = webdriver.Firefox()
    browser.get("https://www.flashscore.com/")

    #closes cookies
    cookies = browser.find_element_by_id("onetrust-accept-btn-handler")
    cookies.click()
    browser.implicitly_wait(2)

    #Identifies search button, searches for desired team, heads to team page
    search_button = browser.find_element_by_css_selector(".header__buttonIcon--search")
    search_button.click()
    search_bar = browser.find_element_by_css_selector("#search-form-query")
    search_bar.send_keys(team)
    browser.implicitly_wait(2)
    result_element = browser.find_element_by_css_selector("#search-results > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > a:nth-child(1)")
    result_element.click()
    browser.implicitly_wait(2)

    #Shows more matches
    show_matches = browser.find_element_by_css_selector(".event__more")
    show_matches.click()
    browser.implicitly_wait(1)

    #Extracts game id's into a list of links
    games = browser.find_elements_by_class_name("event__match")
    game_links = []
    for game in games:
        game_id = game.get_attribute("id")      #it is used, even though it shows it isnt
        game_links.append("https://www.flashscore.com/match/" + game_id[4:] + "/#match-statistics;0")

    #Visits every game stats site and scraps data into lists (huge_list)
    huge_list = []
    for page in game_links[:10]:
        browser.get(page)
        element = browser.find_elements_by_class_name("statTextGroup")      #Necessary, not sure why
        soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
        tag = soup.find_all('div', {"class": "statTextGroup"})
        imena = soup.find_all('div', {"class": "tname__text"})              #Finds team names
        match_time = soup.find_all('div', {"class": "description__time"})   #Finds match date and time
        rezultat = soup.find_all('span', {"class": "scoreboard"})           #Finds match result
        medium_list = [[imena[0].text.strip(), match_time[0].text.strip(), imena[1].text.strip()],
        [rezultat[0].text.strip(), "result", rezultat[1].text.strip()]]     #Createst a list for stats
        for el in tag:      #Loops through all divs with stat. data and extracts it
            stat = []
            mini_list = el.find_all('div')
            for el in mini_list:
                stat.append(el.text)
            medium_list.append(stat)
        huge_list.append(medium_list)
    browser.quit()
    return huge_list
