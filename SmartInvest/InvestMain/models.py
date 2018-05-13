from django.db import models

class Strategy(models.Model):
	userid = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	number_of_stocks_1 = models.IntegerField()
	number_of_stocks_2 = models.IntegerField()
	number_of_stocks_3 = models.IntegerField()