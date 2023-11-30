from django.urls import path
from .views import *

urlpatterns=[
    path('productdet/<int:id>',ProductDetView.as_view(),name="prodet"),
    path('addtocart/<int:id>',AddtoCartView.as_view(),name="acart"),
    path('cartlist',CartlistView.as_view(),name="cartlist"),
    path('remcart/<int:id>',DelCartItemView.as_view(),name="rcart"),
    path('cout/<int:id>',Checkoutview.as_view(),name="cout"),
    path('orders',OrderlistView.as_view(),name="olist"),
    path('corder<int:id>',cancelorder,name="corder"),
    path('addreview/<int:id>',addreview,name="arev")
]