from django.urls import path

from . import views

urlpatterns = [
    path('portfolio', views.stock_portfolio, name='stock_portfolio'),
    path('invest', views.stock_invest_options, name='invest_view'),
    path('trend/portfolio', views.portfolio_trend, name='portfolio_trend')
]