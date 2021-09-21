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

def note(verna, cd_name):
    
    url1 = 'https://fr.wikipedia.org/wiki/'+verna
    url2 = 'https://inpn.mnhn.fr/espece/cd_nom/'+cd_name
    driver2 = webdriver.Firefox(executable_path=r'C:\Users\utilisateur\Desktop\geckodriver.exe', options=options)
    driver = webdriver.Firefox(executable_path=r'C:\Users\utilisateur\Desktop\geckodriver.exe', options=options)
    print("driver fait")
    driver.get(url1)
    driver2.get(url2)
    print('driver cherche')
    
    #Marque une pause pour que l'élément en forme d'icône de fleur soit visible
    pause1 = WebDriverWait(driver, 10000).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div/div/div[1]")))
    print ('driver charge')
    pause2 = WebDriverWait(driver2, 10000).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[11]/div/div[1]/div/div[1]/div[3]/div[2]/div[1]/div/div[2]")))
    #Clique sur l'icône plantae pour chercher les plante envahisante
    doc_inpn = driver2.find_element_by_xpath('/html/body/div[11]/div/div[1]/div/div[1]/div[3]/div[2]/div[1]/div/div[2]').text
    doc_wiki1 = driver.find_element_by_xpath('/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/p[1]').text
    doc_wiki2 = driver.find_element_by_xpath('/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/p[3]').text
    doc_wiki3 = driver.find_element_by_xpath('/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/p[7]').text
    doc_wiki4 = driver.find_element_by_xpath('/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/p[8]').text
    doc_wiki_systematique = driver.find_element_by_xpath('/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/p[9]').text
    
    driver.quit
    driver2.quit
    print("driver close")
    return doc_inpn, doc_wiki1, doc_wiki2, doc_wiki3, doc_wiki4, doc_wiki_systematique

