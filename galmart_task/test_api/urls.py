from django.urls import path
from .views import login, order

urlpatterns = [
    path('login/', login),
    path('order/', order),
]
