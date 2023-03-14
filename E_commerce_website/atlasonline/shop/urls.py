from django.urls import path,re_path
from . import views

urlpatterns = [
    path('',views.index , name="ShopHome"),
    path('food/',views.food , name="food"),
    path('health/',views.health , name="health"),
    path('beauty/',views.beauty , name="beauty"),
    path('clothes/',views.clothes , name="clothes"),
    path('furniture/',views.furniture , name="furniture"),
    path('daily_items/',views.daily_items , name="daily_items"),
    path('appliances/',views.appliances , name="appliances"),
    path('beverages/',views.beverages , name="beverages"),
    path('electronics/',views.electronics , name="electronics"),
    path('sports_equipment/',views.sports_equipment , name="sports_equipment"),
    path('cleaning/',views.cleaning , name="cleaning"),
    path('office/',views.office , name="office"),
    path('medical/',views.medical , name="medical"),
    path('signup/',views.signup , name="signup"),
    path('login/',views.login , name="login"),
    path('logout/',views.logout , name="logout"),
    path('productview/<int:id>',views.prodView , name="productview"),
    path('search/',views.search , name="search"),
    path('checkout/',views.checkout ,name="checkout"),

    # path('cart/',views.cart , name="cart")
    re_path(r'^cart$', views.cart, name='cart')
   
]
