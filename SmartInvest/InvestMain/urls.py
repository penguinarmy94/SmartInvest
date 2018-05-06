from django.urls import path

from . import views

urlpatterns = [
    path('', views.stock_calculator, name='stock_calculator'),
    path('result', views.stock_portfolio, name='stock_portfolio'),
    path('invest', views.stock_invest_options, name='invest_view'),
]