from django.db import models

class Strategy(models.Model):
	userid = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	lookup = models.CharField(max_length=100)
	number_of_stocks_1 = models.IntegerField()
	number_of_stocks_2 = models.IntegerField()
	number_of_stocks_3 = models.IntegerField()
	
	def __str__(self):
		string = self.name + "\n"
		string += ("Share 1: " + str(self.number_of_stocks_1) + "\n")
		string += ("Share 2: " + str(self.number_of_stocks_2) + "\n")
		string += ("Share 3: " + str(self.number_of_stocks_3) + "\n")
		
		return string
		
		
		