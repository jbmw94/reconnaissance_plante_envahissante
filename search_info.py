import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
import shutil
import requests
import os

options = Options()
options.headless = True

URL_WIKIPEDIA = "https://fr.wikipedia.org/wiki/"
URL_INPN = "https://inpn.mnhn.fr/espece/cd_nom/"
GECKODRIVER = r'C:\Users\utilisateur\Desktop\geckodriver.exe'

INPN_XPATH_1 = "/html/body/div/div/div[1]"
INPN_XPATH_2 = "/html/body/div[11]/div/div[1]/div/div[1]/div[3]/div[2]/div[1]/div/div[2]"
WIKI_MAIN_XPATH = '/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/'

def note(verna, cd_name):
    
    url1 = URL_WIKIPEDIA+verna
    url2 = URL_INPN+cd_name
    driver2 = webdriver.Firefox(executable_path=GECKODRIVER, options=options)
    driver = webdriver.Firefox(executable_path=GECKODRIVER, options=options)
    print("driver fait")
    driver.get(url1)
    driver2.get(url2)
    print('driver cherche')
    
    #Marque une pause pour que l'élément en forme d'icône de fleur soit visible
    pause1 = WebDriverWait(driver, 10000).until(EC.visibility_of_element_located((By.XPATH, INPN_XPATH_1)))
    print ('driver charge')
    pause2 = WebDriverWait(driver2, 10000).until(EC.visibility_of_element_located((By.XPATH, INPN_XPATH_2)))
    #Clique sur l'icône plantae pour chercher les plante envahisante
    doc_inpn = driver2.find_element_by_xpath(INPN_XPATH_2).text
    doc_wiki1 = driver.find_element_by_xpath(WIKI_MAIN_XPATH + 'p[1]').text
    doc_wiki2 = driver.find_element_by_xpath(WIKI_MAIN_XPATH + 'p[3]').text
    doc_wiki3 = driver.find_element_by_xpath(WIKI_MAIN_XPATH + 'p[7]').text
    doc_wiki4 = driver.find_element_by_xpath(WIKI_MAIN_XPATH + 'p[8]').text
    doc_wiki_systematique = driver.find_element_by_xpath(WIKI_MAIN_XPATH + 'p[9]').text
    
    driver.quit
    driver2.quit
    print("driver close")
    return doc_inpn, doc_wiki1, doc_wiki2, doc_wiki3, doc_wiki4, doc_wiki_systematique

