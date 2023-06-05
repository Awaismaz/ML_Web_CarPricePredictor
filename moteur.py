
from dateutil.relativedelta import relativedelta
from datetime import date
from bs4 import BeautifulSoup
from requests import get
import pandas as pd


headers = ({'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})

def moteur_get_links(pages):

    ads=[]

    base_url =   "https://www.moteur.ma/fr/voiture/achat-voiture-occasion/"
    
    for i in range(pages):
        if i!=0:
            target_url= base_url + "{}".format(15*i)
        else:
            target_url= base_url
        response = get(target_url, headers=headers)


        html_soup = BeautifulSoup(response.text, 'html.parser')

        divs = html_soup.find_all('div', {'class': "inner ads_info viewstats"})

        for div in divs:
            links = div.find_all('a')
            for a in links:
                ads.append(a['href'])

    return ads

def moteur_get_details(Ad_link):
    ad_dict={}


    response = get(Ad_link, headers=headers)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    div=html_soup.find_all('div', {'class': "col-md-12 col-sm-12 col-xs-12 text-center ads-detail"})[0]
    name=html_soup.find_all('span', {'class': "text_bold"})[0].text.strip()

    nomenclature=name.split()

    ad_dict['Brand']=nomenclature[0]

    Model=''

    for i,nom in enumerate(nomenclature):
        if i==0:
            pass
        elif i==1:
            Model+=nom
        else:
            Model+=' ' + nom

    ad_dict['Model and Version']=Model

    divs=html_soup.find_all('div', {'class': "actions block_tele"})

    for div in divs:
        As=div.find_all('a')
        break

    ad_dict['Seller name']=As[0].text.strip()

    for A in As:
        if "icon icon-normal-pointer" in str(A):
            ad_dict['City']=A.text.strip()

    try:
        ad_dict['Price']=html_soup.find_all('div', {'class': "color_primary text_bold price-block"})[0].text.strip()
    except:
        ad_dict['Price']=''            

    divs=html_soup.find_all('div', {'class': "detail_line"})

    for div in divs:
        spans=div.find_all('span')

        if spans[0].text== 'Kilométrage':  
            ad_dict['Mileage']= spans[1].text.replace('\n','').replace('\t','').replace('\r','')

        elif spans[0].text== 'Année':  
            ad_dict['Year']= spans[1].text.replace(' ','')


        elif spans[0].text== 'Boite de vitesses':  
            ad_dict['Gearbox']= spans[1].text.replace('\n','').replace('\t','').replace('\r','')

        elif spans[0].text== 'Carburant':  
            ad_dict['Fuel']= spans[1].text.replace('\n','').replace('\t','').replace('\r','')

        elif spans[0].text== 'Date':  
            ad_dict['Date']= spans[1].text.replace('\n','').replace('\t','').replace('\r','')

        elif spans[0].text== 'Puissance fiscale':  
            ad_dict['Fiscal Power']= spans[1].text.replace(' ','')

        elif spans[0].text== 'Nombre de portes':  
            ad_dict['Doors']= spans[1].text.replace(' ','')

        elif spans[0].text== 'Carrosserie':  
            ad_dict['Body']= spans[1].text.replace('\n','').replace('\t','').replace('\r','')

        elif spans[0].text== 'Première main':  
            ad_dict['First Hand']= spans[1].text.replace('\n','').replace('\t','').replace('\r','')



    ad_dict['Ad Link']=Ad_link

    return ad_dict

def moteur_update():
    print("Fetching Latest data from moteur.ma")
    total_ads=200

    pages=(total_ads//15)

    if total_ads%15!=0:
        pages+=1


    ads=moteur_get_links(pages)

    ads=list(set(ads))


    data=[]
    for ad in ads:
        try:
            result=moteur_get_details(ad)
            data.append(result)
        except:
            pass
    
    df=pd.DataFrame(data)

    df.to_csv('Moteur_data.csv')

if __name__=="__main__":
    moteur_update()