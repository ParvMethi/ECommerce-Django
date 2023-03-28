from django.urls import path
from carts.views import cart

urlpatterns = [
    path('', cart, name='cart'),

]