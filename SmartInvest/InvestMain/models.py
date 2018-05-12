from django.db import models

class Portfolio:
	userid = models.CharField()
	strategies = models.CharField()
	stock_count = models.CharField()