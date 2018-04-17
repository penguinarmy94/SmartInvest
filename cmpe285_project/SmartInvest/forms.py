from django import forms

class StockCalculatorForm(forms.Form):
	symbol = forms.CharField(max_length = 4)
	allotmet = forms.IntegerField()
	final_share_price = forms.IntegerField()
	sell_commission = forms.IntegerField()
	initial_share_price = forms.IntegerField()
	buy_commission = forms.IntegerField()
	capital_gain_tax_rate = forms.IntegerField()
	