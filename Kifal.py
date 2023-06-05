
from dateutil.relativedelta import relativedelta
from datetime import date
from bs4 import BeautifulSoup
from requests import get
import pandas as pd


headers = ({'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})

def kifal_get_links(pages):

    ads=[]

    base_url =   "https://kifal-auto.ma/annonces"
    
    for i in range(pages):
        if i!=0:
            target_url= base_url + "?page={}".format(i+1)
        else:
            target_url= base_url
        response = get(target_url, headers=headers)


        html_soup = BeautifulSoup(response.text, 'html.parser')

        divs = html_soup.find_all('div', {'class': "col-lg-6 col-md-6 col-xl-6"})

        for div in divs:
            links = div.find_all('a')
            for a in links:
                ads.append(a['href'])

    return ads

def kifal_get_details(Ad_link):
    ad_dict={}


    response = get(Ad_link, headers=headers)
    html_soup = BeautifulSoup(response.text, 'html.parser')


    ad_dict['Title'] = html_soup.find_all('div', {'class': "h3 mb-0"})[0].text

    div=html_soup.find_all('div', {'class': "h3 font-weight-bold mb-0 text-center"})[0]
    ad_dict['Price'] = div.find_all('span')[0].text.replace("\n", "")
    
    divs=html_soup.find_all('div','col-12 col-md-4 col-lg-3 text-center')
    
    ad_dict['Make and Model']=divs[0].find_all('p')[0].text.replace('\n','')
    ad_dict['Fuel']=divs[1].find_all('p')[0].text.replace('\n','')
    ad_dict['Gearbox']=divs[2].find_all('p')[0].text.replace('\n','')
    ad_dict['City']=divs[3].find_all('p')[0].text.replace('\n','')


    divs=html_soup.find_all('div', {'class': "d-flex justify-content-between border-bottom"})

    for div in divs:
        spans=div.find_all('span')

        if spans[0].text.replace('\n','')== 'Année':  
            ad_dict['Year']= spans[1].text.replace('\n','')

        elif spans[0].text.replace('\n','')== 'Puissance fiscale':  
            ad_dict['Fiscal Power']= spans[1].text.replace('\n','')

        elif spans[0].text.replace('\n','')== 'Kilométrage':  
            ad_dict['Mileage']= spans[1].text.replace('\n','')

        elif spans[0].text.replace('\n','')== 'Origine':  
            ad_dict['Origin']= spans[1].text.replace('\n','')

        elif spans[0].text.replace('\n','')== 'Type de voiture':  
            ad_dict['Type of Car']= spans[1].text.replace('\n','')

        elif spans[0].text.replace('\n','')== 'la finition':  
            ad_dict['Finish']= spans[1].text.replace('\n','')

        elif spans[0].text.replace('\n','')== 'la finition':  
            ad_dict['Engine']= spans[1].text.replace('\n','')

        elif spans[0].text.replace('\n','')== 'Première main':  
            if spans[1].text.replace('\n','') == 'Oui':
                ad_dict['First Hand']= True
            else:
                ad_dict['First Hand']= False




    ad_dict['Description']=html_soup.find_all('div', {'class': "justify-content mb-4"})[0].text.replace('\n','')

    divs=html_soup.find_all('div', {'class': "d-flex justify-content-between px-2 py-1 shadow-sm rounded-lg"})

    features=[]
    start=0
    for div in divs:
        span=div.find_all('span', {'class': "text-muted-dark"})[0].text.replace('\n','')
        
        if start==1:
            features.append(span)        
        
        if span=='Kw':
            start=1


    ad_dict['Features (Interior comfort, Driving assistance, Multimedia, Exterior aspects, Safety'] = features

    ad_dict['Ad Link']=Ad_link

    # import json

    # data = json.loads(html_soup.find('script', type='application/json', id="__NEXT_DATA__").text)

    # ad_dict['Contact']=(data['props']['pageProps']['componentProps']['adInfo']['ad']['phone'])

    return ad_dict



def kifal_update():
    print("Fetching Latest data from Kifal.ma")
    total_ads=200

    pages=(total_ads//10) + 1

    ads=kifal_get_links(pages)

    ads=list(set(ads))

    data=[]
    for ad in ads:
        try:
            result=kifal_get_details(ad)
            data.append(result)
        except:
            pass
    
    df=pd.DataFrame(data)

    df.to_csv('Kifal_data.csv')

if __name__=="__main__":
    kifal_update()
