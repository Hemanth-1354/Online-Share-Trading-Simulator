# forms.py

from django import forms

class StockSearchForm(forms.Form):
    search_name = forms.CharField(label='Search Stock Symbol', max_length=10, required=True)
