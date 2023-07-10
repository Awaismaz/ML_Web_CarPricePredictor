from django.shortcuts import render,redirect
from django.views.generic import (TemplateView, ListView, )
from car_ads.models import ad
import pandas as pd
import numpy as np
from urllib.parse import urlparse
from django.urls import reverse
import joblib
# Create your views here.
from django.db.models import F, Func, FloatField, ExpressionWrapper
from django.db.models.functions import Cast

class ads(TemplateView):

    template_name = 'ads.html'

    def get_context_data(self,*args, **kwargs):
        context = super(ads, self).get_context_data(*args,**kwargs)
        context['ads'] = ad.objects.all()
        context['qty'] = ad.objects.all().count()
        brands = ad.objects.order_by('brand').values_list('brand', flat=True).distinct()
        context['brands']=brands
        fuels = ad.objects.order_by('fuel').values_list('fuel', flat=True).distinct()
        context['fuels']=fuels
        x=self.request.GET.get('trained')
        if x=='1':
            context['trained']=1
        y=self.request.GET.get('prediction')
        if y is not None:
            context['prediction']=y
            reference_price_float=float(y)
            cars_queryset = ad.objects.exclude(price__exact='nan').annotate(
                price_diff=Cast(F('price'), FloatField()) - reference_price_float,
            )

            # Sort the queryset by the absolute difference in ascending order and retrieve the top 10 closest matches
            closest_matches = cars_queryset.order_by('price_diff')[:10]
            
            context['matches']=closest_matches
        
        return context

def brand_unique(x):
    if x=='ALFA' or x=='ALFA-ROMEO':
        return 'ALFA ROMEO'
    elif x=='MERCEDES' or x=='MERCEDES-BENZ':
        return 'MERCEDES BENZ'
    elif x=='LAND-ROVER':
        return 'LAND ROVER'
    else:
        return x

def First_hand(x):
    if x=='True' or x=='Oui' or x=='TRUE'or x==True:
        return 'Yes'
    else:
        return 'No'

def Gearbox(x):
    if x=='Automatique' or x==' Automatique':
        return 'Automatic'
    else:
        return 'Manual'

def Fuel(x):
    if x=='Diesel' or x=='Diesel ' or x==' Diesel':
        return 'diesel'
    elif x=='Essence':
        return 'gasoline'
    elif x=='Hybride':
        return 'hybrid'    
    elif x=='Electrique':
        return 'electric' 
    else:
        return 'gasoline'


def csv_to_df():

    df1=pd.read_csv('Kifal_data.csv')
    df2=pd.read_csv('Moteur_data.csv')
    df3=pd.read_csv('Avito_data.csv')
    df4=pd.read_csv('autocaz.csv')


    df1['brand']=df1['Make and Model'].apply(lambda x: x.split(' ')[0])
    df1['model']=df1['Make and Model'].apply(lambda x: x.split(' ')[1])
    df1=df1.drop(columns=['Make and Model', 'City', 'Origin','Type of Car','Title', 'Finish', 'Description','Features (Interior comfort, Driving assistance, Multimedia, Exterior aspects, Safety'])

    def df1_price(x):
        if pd.isna(x):
            return np.nan
        else:
            return x.split(' ')[0]+x.split(' ')[1]  

    df1['Price']=df1['Price'].fillna('- -').apply(lambda x: df1_price(x))
    df1['Mileage']=df1['Mileage'].str.replace("km", "")
    df1['Mileage']=df1['Mileage'].str.replace(" ", "")


    def df2_price(x):
        if pd.isna(x):
            return np.nan
        else:
            return x.split(' ')[0]+x.split(' ')[1]
    
    df2['brand']=df2['Brand']
    df2['model']=df2['Model and Version']
    df2=df2.drop(columns=['Brand','Date', 'City', 'Seller name','Model and Version','Body','Doors'])

    df2['Price']=df2['Price'].apply(lambda x: df2_price(x))
    df2['Mileage']=df2['Mileage'].str.replace(" ", "")

    
    df3['brand']=df3['Make']
    df3['model']=df3['Model']
    df3['Year']=df3['Year-Model']
    df3=df3.drop(columns=['Year-Model','Condition','Make','Origin','Advertiser','Title', 'City', 'Type','Model','Description','Equipment','Ad Date','Contact','Sector'])

    def df3_mileage(x):
        if pd.isna(x):
            return np.nan
        else:
            return x.split(' - ')[0].replace(" ", "")

    def df3_fiscal(x):
        if pd.isna(x):
            return np.nan
        else:
            return x.split(' ')[0]

    def df3_price(x):
        if pd.isna(x):
            return np.nan
        else:
            return str(int(x))

    df3['Mileage']=df3['Mileage'].apply(lambda x: df3_mileage(x))
    df3['Price']=df3['Price'].apply(lambda x: df3_price(x))
    df3['Fiscal Power']=df3['Fiscal Power'].apply(lambda x: df3_fiscal(x))



    def df4_price(x):
        if pd.isna(x):
            return np.nan
        else:
            return x.split(' ')[0]+x.split(' ')[1]
        
    df4['Price']=df4['price']
    df4['Year']=df4['year']
    df4['model']=df4['Model']
    df4=df4.drop(columns=['year','price','Model','Date of CME','Color','Category', 'Doors', 'Seats'])

    df4['Price']=df4['Price'].apply(lambda x: df4_price(x))

    df=pd.concat([df1,df2,df3,df4],ignore_index = True)
    
    
    size = len(df)
    for i in range (size):
        try:
            if len(df.loc[i]['brand'])==0:
                df.iloc[i, df.columns.get_loc('brand')]=df.loc[i]['model']
        except:
            df.iloc[i, df.columns.get_loc('brand')]=df.loc[i]['model']
    
    df = df[df['brand'].notna()]

    df['brand']=df['brand'].apply(lambda x: x.upper())
    df['brand']=df['brand'].apply(lambda x: brand_unique(x))

    df['First Hand']=df['First Hand'].apply(lambda x: First_hand(x))
    df['Gearbox']=df['Gearbox'].apply(lambda x: Gearbox(x))
    df['Fuel']=df['Fuel'].apply(lambda x: Fuel(x))

    return df

def update(request):

    ad.objects.all().delete()
    df=csv_to_df()
    size = len(df)

    for i in range (size):

        try:
            entry = ad (       
                                ad_link = df.loc[i]['Ad Link'],
                                brand = df.loc[i]['brand'],
                                model = df.loc[i]['model'],
                                mileage = df.loc[i]['Mileage'],
                                year = df.loc[i]['Year'],
                                platform = urlparse(df.loc[i]['Ad Link']).netloc,
                                gearbox = df.loc[i]['Gearbox'],
                                price=df.loc[i]['Price'],
                                fiscal_power=df.loc[i]['Fiscal Power'],
                                fh=df.loc[i]['First Hand'],
                                fuel=df.loc[i]['Fuel'],
                        )
            entry.save()
        except:
            pass
    

    return redirect ('/')

def train(request):
    df=csv_to_df()
    df=df.dropna()
    
    from sklearn import preprocessing
    le1 = preprocessing.LabelEncoder()
    le2 = preprocessing.LabelEncoder()
    df['brand'] = le1.fit_transform(df['brand'])
    df['Fuel'] = le2.fit_transform(df['Fuel'])
    
    def First_hand(x):
        if x=='Yes':
            return 1
        else:
            return 0

    df['First Hand']=df['First Hand'].apply(lambda x: First_hand(x))

    def Gearbox(x):
        if x=='Automatic':
            return 1
        else:
            return 0
        
    df['Gearbox']=df['Gearbox'].apply(lambda x: Gearbox(x))
    df=df.drop(columns=['Ad Link', 'model'])
    df['Price']=df['Price'].astype(float)
    df['Gearbox']=df['Gearbox'].astype(float)
    df['Year']=df['Year'].astype(float)
    df['Fiscal Power']=df['Fiscal Power'].astype(float)
    df['Mileage']=df['Mileage'].astype(float)
    df['First Hand']=df['First Hand'].astype(float)
    df['brand']=df['brand'].astype(float)
    df['Fuel']=df['Fuel'].astype(float)


    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn import metrics
    import numpy as np
    X_train, X_test, y_train, y_test = train_test_split(df.drop(columns=['Price']), df['Price'], test_size=0.3, random_state=100)
    lm = LinearRegression()
    lm.fit(X_train,y_train)

    # predictions = lm.predict(X_test)
    # print(predictions)

    joblib.dump(lm, 'model.pkl')
    joblib.dump(le1, 'brand_encoder.pkl')
    joblib.dump(le2, 'fuel_encoder.pkl')

    redirect_url = reverse('car_ads:ads') + "?trained=1"

    return redirect (redirect_url)

def predict(request):

    if request.method == 'POST':
        model = joblib.load('model.pkl')
        brand_encoder = joblib.load('brand_encoder.pkl')
        fuel_encoder = joblib.load('fuel_encoder.pkl')

        fuel = request.POST.get('fuel')
        gearbox = request.POST.get('gearbox')
        year = request.POST.get('year')
        fiscal_power = request.POST.get('fiscal_power')
        mileage = request.POST.get('mileage')
        first_hand = request.POST.get('first_hand')
        brand = request.POST.get('brand')
        
        if first_hand=='Yes':
            first_hand=1
        else:
            first_hand=0

        if gearbox=='Automatic':
            gearbox=1
        else:
            gearbox=0

        brand = brand_encoder.transform([brand])[0]
        fuel = fuel_encoder.transform([fuel])[0]
        my_list = [fuel, gearbox, year, fiscal_power, mileage, first_hand, brand]
        float_list = [float(x) for x in my_list]
        X = [float_list]

        # Make predictions using the loaded model
        prediction = model.predict(X) - 15000

    prediction=str(int(np.round(prediction)[0]))
    redirect_url = reverse('car_ads:ads') + "?prediction=" + prediction

    return redirect (redirect_url)