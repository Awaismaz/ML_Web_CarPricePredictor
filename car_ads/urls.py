from django.urls import path
from car_ads import views
from django.views.static import serve

app_name= 'car_ads'

urlpatterns = [
    path('', views.ads.as_view(), name='ads'),
    path('update', views.update, name='update'),
    path('train', views.train, name='train'),
    path('predict', views.predict, name='predict'),
    path('get_models/', views.get_models, name='get_models'),
]