from django.core.management.base import BaseCommand
from API.models import Stock
from decimal import Decimal

class Command(BaseCommand):
    help = 'Add additional US and Indian stocks'

    def handle(self, *args, **kwargs):
        stocks_to_add = [
            # US Stocks
            {'symbol': 'NVDA', 'name': 'NVIDIA Corporation', 'price': Decimal('875.35')},
            {'symbol': 'AMD', 'name': 'Advanced Micro Devices', 'price': Decimal('178.90')},
            {'symbol': 'INTC', 'name': 'Intel Corporation', 'price': Decimal('42.75')},
            {'symbol': 'CRM', 'name': 'Salesforce', 'price': Decimal('307.78')},
            {'symbol': 'PYPL', 'name': 'PayPal Holdings', 'price': Decimal('62.45')},
            {'symbol': 'DIS', 'name': 'The Walt Disney Company', 'price': Decimal('111.95')},
            {'symbol': 'PFE', 'name': 'Pfizer Inc.', 'price': Decimal('27.85')},
            {'symbol': 'KO', 'name': 'The Coca-Cola Company', 'price': Decimal('59.85')},
            {'symbol': 'WMT', 'name': 'Walmart Inc.', 'price': Decimal('60.45')},
            {'symbol': 'BAC', 'name': 'Bank of America', 'price': Decimal('34.75')},
            {'symbol': 'VZ', 'name': 'Verizon Communications', 'price': Decimal('40.85')},
            {'symbol': 'CSCO', 'name': 'Cisco Systems', 'price': Decimal('49.75')},
            {'symbol': 'NFLX', 'name': 'Netflix, Inc.', 'price': Decimal('628.85')},
            {'symbol': 'PEP', 'name': 'PepsiCo, Inc.', 'price': Decimal('171.95')},
            {'symbol': 'ADBE', 'name': 'Adobe Inc.', 'price': Decimal('485.75')},

            # Indian Stocks
            {'symbol': 'HDFCBANK', 'name': 'HDFC Bank Limited', 'price': Decimal('1456.75')},
            {'symbol': 'ICICIBANK', 'name': 'ICICI Bank Limited', 'price': Decimal('1023.45')},
            {'symbol': 'SBIN', 'name': 'State Bank of India', 'price': Decimal('624.85')},
            {'symbol': 'BHARTIARTL', 'name': 'Bharti Airtel Limited', 'price': Decimal('1167.90')},
            {'symbol': 'ASIANPAINT', 'name': 'Asian Paints Limited', 'price': Decimal('2845.75')},
            {'symbol': 'HINDUNILVR', 'name': 'Hindustan Unilever', 'price': Decimal('2456.85')},
            {'symbol': 'MARUTI', 'name': 'Maruti Suzuki India', 'price': Decimal('10245.75')},
            {'symbol': 'AXISBANK', 'name': 'Axis Bank Limited', 'price': Decimal('978.45')},
            {'symbol': 'WIPRO', 'name': 'Wipro Limited', 'price': Decimal('423.85')},
            {'symbol': 'HCLTECH', 'name': 'HCL Technologies', 'price': Decimal('1245.75')},
            {'symbol': 'SUNPHARMA', 'name': 'Sun Pharmaceutical', 'price': Decimal('1167.85')},
            {'symbol': 'BAJFINANCE', 'name': 'Bajaj Finance', 'price': Decimal('6789.75')},
            {'symbol': 'TITAN', 'name': 'Titan Company Limited', 'price': Decimal('3456.85')},
            {'symbol': 'ULTRACEMCO', 'name': 'UltraTech Cement', 'price': Decimal('8967.75')},
            {'symbol': 'KOTAKBANK', 'name': 'Kotak Mahindra Bank', 'price': Decimal('1756.85')},
        ]

        for stock_data in stocks_to_add:
            Stock.objects.get_or_create(
                symbol=stock_data['symbol'],
                defaults={
                    'name': stock_data['name'],
                    'price': stock_data['price']
                }
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully added stock {stock_data["symbol"]}')
            )