from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import bs4
import requests
import time
import csv
import pandas
import os.path
from os import path

#Prints stats to a csv file, and returns True; if game already is already saved, returns False
def stats_to_csv(stat_list, team_name):
    date = stat_list[0][0][:10].replace(".", "-")
    file_name = "data/{}-{}.csv".format(team_name, date)      #Assembles filename
    frame = pandas.DataFrame.from_records(stat_list[1:], columns = ["category", *stat_list[0][1:]])
    if not path.exists(file_name):
        frame.to_csv(file_name, index = False)
        return True
    else:
        return False

#Visits a page and scraps match stats, returns list with stats
def get_match_stats(page):
    browser = webdriver.Firefox()
    browser.get(page)
    element = browser.find_elements_by_class_name("statTextGroup")      #Necessary, not sure why
    browser.implicitly_wait(50)
    soup = bs4.BeautifulSoup(browser.page_source, "html.parser")
    tag = soup.find_all('div', {"class": "statTextGroup"})
    imena = soup.find_all('div', {"class": "tname__text"})              #Finds team names
    match_time = soup.find_all('div', {"class": "description__time"})   #Finds match date and time
    rezultat = soup.find_all('span', {"class": "scoreboard"})           #Finds match result
    medium_list = [[match_time[0].text.strip(), imena[0].text.strip(), imena[1].text.strip()],
    ["result", rezultat[0].text.strip(), rezultat[1].text.strip()]]     #Createst a list for stats
    for el in tag:      #Loops through all divs with stat. data and extracts it
        stat = []
        mini_list = el.find_all('div')
        for el in mini_list:
            stat.append(el.text)
        medium_list.append([stat[1], stat[0], stat[2]])                  #Changes the order of data (more organised)
    browser.quit()
    return medium_list

#Updates match history files, adding games that aren't saved yet
def update_match_history(team):
        
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

    browser.quit()      #We don't need it anymore, we will be opening new ones anyway

    #Visits every game stats site and scraps data into lists (huge_list)
    stat_list = []
    for page in game_links[:20]:                  
        statistics = get_match_stats(page)
        if not stats_to_csv(statistics, team):
            break
        stat_list.append(get_match_stats(page))
    browser.quit()
    return stat_list

