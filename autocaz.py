
from dateutil.relativedelta import relativedelta
from datetime import date
from bs4 import BeautifulSoup
from requests import get
import pandas as pd


headers = ({'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
browser = webdriver.Chrome('chromedriver.exe')

def autocaz_get_links():

    browser.get("https://autocaz.ma/search-result?page=1&size=10")
    time.sleep(5)

    elem = browser.find_element(By.TAG_NAME, "body")

    no_of_pagedowns = 20

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        no_of_pagedowns-=1

    ad = browser.find_element(By.CLASS_NAME,"scroll")
    links=ad.find_elements(By.TAG_NAME,"a")

    ads=[]
    
    for link in links:
        ads.append(link.get_attribute('href'))

    return ads

def autocaz_get_details(Ad_link):

   
    ad_dict={}

    browser.get(Ad_link)
    time.sleep(2)

    options = browser.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div/div/div/div/div[3]/div[2]")
    # options = browser.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div/div/div/div/div[3]/div[2]")

    names = options.find_elements(By.TAG_NAME,"p")
    
    ad_dict['price']=browser.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div/div/div/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/h5").text

    features=[]
    attributes=[]

    for i,name in enumerate(names):
        if i%2==0:
            if name.text=='Marque':
                features.append('brand')
            elif name.text=='Modèle':
                features.append('Model')
            elif name.text=='Date de MEC':
                features.append('Date of CME')
            elif name.text=='Couleur':
                features.append('Color')
            elif name.text=='Catégorie':
                features.append('Category')
            elif name.text=='Kilométrage':
                features.append('Mileage')
            elif name.text=='Carburant':
                features.append('Fuel')
            elif name.text=='Portes':
                features.append('Doors')
            elif name.text=='Places':
                features.append('Seats')
            elif name.text=='Puissance fiscale':
                features.append('Fiscal Power')
            elif name.text=='Boite de vitesse':
                features.append('Gearbox')
            elif name.text=='Première main':
                features.append('First Hand')

        else:
            attributes.append(name.text)

    for i in range(len(features)):
        if features[i]=='Mileage':
            attributes[i]=attributes[i].replace("\u202f",'')
        ad_dict[features[i]]=attributes[i]
        
    ad_dict['Ad Link']=Ad_link

    ad_dict['year']=ad_dict['Date of CME'].split('/')[2]



    return ad_dict

def autocaz_update():
    print("Fetching Latest data from autocaz.ma")
    ads=autocaz_get_links()

    ads=list(set(ads))

    data=[]
    result=autocaz_get_details(ads[0])
    data.append(result)
    # for ad in ads:
    #     try:
    #         result=autocaz_get_details(ad)
    #         data.append(result)
    #     except:
    #         pass
    
    df=pd.DataFrame(data)

    df.to_csv('autocaz.csv')

if __name__=="__main__":
    autocaz_update()

