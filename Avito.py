
from dateutil.relativedelta import relativedelta
from datetime import date
from bs4 import BeautifulSoup
from requests import get
import pandas as pd

headers = ({'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})

def avito_get_links(pages):

    ads=[]

    base_url =   "https://www.avito.ma/fr/maroc/voitures-%C3%A0_vendre"
    
    for i in range(pages):
        if i!=0:
            target_url= base_url + "?o={}".format(i+1)
        else:
            target_url= base_url
        response = get(target_url, headers=headers)


        html_soup = BeautifulSoup(response.text, 'html.parser')

        divs = html_soup.find_all('div', {'class': "listing"})

        for div in divs:
            links = div.find_all('a')
            for a in links:
                ads.append(a['href'])

    return ads

def avito_get_details(Ad_link):
    ad_dict={}


    response = get(Ad_link, headers=headers)
    html_soup = BeautifulSoup(response.text, 'html.parser')

    divs = html_soup.find_all('div', {'class': "sc-uaojr6-4 eicSBc"})
    for div in divs:
        results = div.find_all('p')
        for result in results:
            ad_dict['Advertiser']=result.text


    divs = html_soup.find_all('div', {'class': "sc-1g3sn3w-9 gIlAYt"})
    for div in divs:
        results = div.find_all('h1')
        for result in results:
            ad_dict['Title']=result.text

    divs = html_soup.find_all('div', {'class': "sc-1g3sn3w-10 iMiMHk"})
    for div in divs:
        results = div.find_all('p')
        for result in results:
            ad_dict['Price']=(result.text).replace('\u202f','').split()[0]
            if ad_dict['Price'] == 'Prix':
                ad_dict['Price'] = ''

    divs = html_soup.find_all('div', {'class': "sc-1g3sn3w-7 NuEic"})
    for div in divs:
        results = div.find_all('span')
        for result in results:
            ad_dict['City']=result.text
            break

    divs = html_soup.find_all('div', {'class': "sc-6p5md9-2 dhFfvW"})
    for div in divs:
        results = div.find_all('span')
        for result in results:
            if result.text[0].isdigit():
                ad_dict['Fiscal Power']=result.text
            elif result.text[0]=='M' or result.text[0]=='A':
                ad_dict['Gearbox']=result.text
            else:
                ad_dict['Fuel']=result.text

    ad_dict['Type']='Used cars for sale'

    lis = html_soup.find_all('li', {'class': "sc-qmn92k-1 ldnQxr"})
    
    for li in lis:
        results = li.find_all('span')
        if results[0].text=='Secteur':
            ad_dict['Sector']=results[1].text
        elif results[0].text=='Modèle':
            ad_dict['Model']=results[1].text        
        elif results[0].text=='Année-Modèle':
            ad_dict['Year-Model']=results[1].text   
        elif results[0].text=='Première main':
            if results[0].text[0]=='N':   
                ad_dict['First Hand']=False
            else:
                ad_dict['First Hand']=True
        elif results[0].text=='Origine':
            ad_dict['Origin']=results[1].text   
        elif results[0].text=='État':
            ad_dict['Condition']=results[1].text   
        elif results[0].text=='Marque':
            ad_dict['Make']=results[1].text   
        elif results[0].text=='Kilométrage':
            ad_dict['Mileage']=results[1].text 

    divs = html_soup.find_all('div', {'class': "sc-1g3sn3w-16 leVIwi"})
    for div in divs:
        results = div.find_all('p')
        for result in results:
            ad_dict['Description']=result.text
            break

    features=[]
    divs = html_soup.find_all('div', {'class': "sc-mnh93t-2 eUedZU"})
    for div in divs:
        results = div.find_all('span')
        for result in results:
            features.append(result.text)
            break

    ad_dict['Equipment']=features

    ad_dict['Ad Link']=Ad_link

    divs = html_soup.find_all('div', {'class': "sc-1g3sn3w-7 NuEic"})
    for div in divs:
        results = div.find_all('span')
        for i,result in enumerate(results):
            if i==0:
                pass
            else:
                frame=result.text.split()[-1]
                diff=int(result.text.split()[3])
                if frame=='minutes':
                    today = date.today()
                    Ad_Date = today - relativedelta(minutes=diff)
                    ad_dict['Ad Date']=Ad_Date.strftime('%m/%d/%Y')

                elif frame=='heures':
                    today = date.today()
                    Ad_Date = today - relativedelta(hours=diff)
                    ad_dict['Ad Date']=Ad_Date.strftime('%m/%d/%Y')

                elif frame=='jours':
                    today = date.today()
                    Ad_Date = today - relativedelta(days=diff)
                    ad_dict['Ad Date']=Ad_Date.strftime('%m/%d/%Y')

                elif frame=='semaines':
                    today = date.today()
                    Ad_Date = today - relativedelta(weeks=diff)
                    ad_dict['Ad Date']=Ad_Date.strftime('%m/%d/%Y')
                else:
                    ad_dict['Ad Date']=''





    import json

    data = json.loads(html_soup.find('script', type='application/json', id="__NEXT_DATA__").text)

    ad_dict['Contact']=(data['props']['pageProps']['componentProps']['adInfo']['ad']['phone'])

    return ad_dict

def avito_update():
    print("Fetching Latest data from Avito.ma")
    total_ads=200

    pages=(total_ads//35) + 1

    ads=avito_get_links(pages)

    ads=list(set(ads))

    data=[]
    for ad in ads:
        try:
            result=avito_get_details(ad)
            data.append(result)
        except:
            pass
    
    df=pd.DataFrame(data)

    df.to_csv('Avito_data.csv')

if __name__=="__main__":
    avito_update()

