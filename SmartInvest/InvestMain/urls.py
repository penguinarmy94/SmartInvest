from django.urls import path

from . import views

urlpatterns = [
    path('result', views.stock_portfolio, name='stock_portfolio'),
    path('invest', views.stock_invest_options, name='invest_view'),
    path('test', views.test_route, name='test_path'),
]