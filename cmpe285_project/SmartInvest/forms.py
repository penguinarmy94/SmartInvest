from django import forms

class StockCalculatorForm(forms.Form):
	symbol = forms.CharField()
	allotment = forms.IntegerField(min_value=0)
	final_share_price = forms.FloatField(min_value=0)
	sell_commission = forms.FloatField(min_value=0)
	initial_share_price = forms.FloatField(min_value=0)
	buy_commission = forms.FloatField(min_value=0)
	capital_gain_tax_rate = forms.FloatField(max_value=100, min_value=0)
	