from django.core.management.base import BaseCommand
from API.models import Stock
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populates the database with static stock data'

    def handle(self, *args, **kwargs):
        stocks = [
            # Tech Stocks
            {'symbol': 'AAPL', 'name': 'Apple Inc.',
                'price': Decimal('175.00')},
            {'symbol': 'MSFT', 'name': 'Microsoft Corporation',
                'price': Decimal('420.00')},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.',
                'price': Decimal('150.00')},
            {'symbol': 'AMZN', 'name': 'Amazon.com Inc.',
                'price': Decimal('180.00')},
            {'symbol': 'META', 'name': 'Meta Platforms Inc.',
                'price': Decimal('500.00')},
            {'symbol': 'TSLA', 'name': 'Tesla Inc.',
                'price': Decimal('170.00')},
            {'symbol': 'NVDA', 'name': 'NVIDIA Corporation',
                'price': Decimal('900.00')},
            {'symbol': 'INTC', 'name': 'Intel Corporation',
                'price': Decimal('42.00')},
            {'symbol': 'IBM', 'name': 'International Business Machines',
                'price': Decimal('190.00')},
            {'symbol': 'ORCL', 'name': 'Oracle Corporation',
                'price': Decimal('125.00')},

            # Indian Stocks - Banking
            {'symbol': 'RELIANCE', 'name': 'Reliance Industries Limited',
                'price': Decimal('2800.00')},
            {'symbol': 'TCS', 'name': 'Tata Consultancy Services',
                'price': Decimal('3800.00')},
            {'symbol': 'HDFCBANK', 'name': 'HDFC Bank Limited',
                'price': Decimal('1500.00')},
            {'symbol': 'INFY', 'name': 'Infosys Limited',
                'price': Decimal('1500.00')},
            {'symbol': 'ICICIBANK', 'name': 'ICICI Bank Limited',
                'price': Decimal('1000.00')},
            {'symbol': 'HINDUNILVR', 'name': 'Hindustan Unilever Limited',
                'price': Decimal('2500.00')},
            {'symbol': 'SBIN', 'name': 'State Bank of India',
                'price': Decimal('600.00')},
            {'symbol': 'BHARTIARTL', 'name': 'Bharti Airtel Limited',
                'price': Decimal('1100.00')},
            {'symbol': 'KOTAKBANK', 'name': 'Kotak Mahindra Bank Limited',
                'price': Decimal('1700.00')},
            {'symbol': 'BAJFINANCE', 'name': 'Bajaj Finance Limited',
                'price': Decimal('7000.00')},

            # Additional Indian Stocks - IT & Tech
            {'symbol': 'WIPRO', 'name': 'Wipro Limited',
                'price': Decimal('450.00')},
            {'symbol': 'TECHM', 'name': 'Tech Mahindra Limited',
                'price': Decimal('1200.00')},
            {'symbol': 'HCLTECH', 'name': 'HCL Technologies Limited',
                'price': Decimal('1300.00')},

            # Additional Indian Stocks - Banking & Finance
            {'symbol': 'AXISBANK', 'name': 'Axis Bank Limited',
                'price': Decimal('1000.00')},
            {'symbol': 'INDUSINDBK', 'name': 'IndusInd Bank Limited',
                'price': Decimal('1400.00')},

            # Additional Indian Stocks - Automobile
            {'symbol': 'MARUTI', 'name': 'Maruti Suzuki India Limited',
                'price': Decimal('10000.00')},
            {'symbol': 'TATAMOTORS', 'name': 'Tata Motors Limited',
                'price': Decimal('800.00')},
            {'symbol': 'M&M', 'name': 'Mahindra & Mahindra Limited',
                'price': Decimal('1700.00')},

            # Additional Indian Stocks - FMCG
            {'symbol': 'ITC', 'name': 'ITC Limited',
                'price': Decimal('400.00')},
            {'symbol': 'NESTLEIND', 'name': 'Nestle India Limited',
                'price': Decimal('2500.00')},

            # Additional Indian Stocks - Pharma
            {'symbol': 'SUNPHARMA', 'name': 'Sun Pharmaceutical Industries Limited',
                'price': Decimal('1200.00')},
            {'symbol': 'DRREDDY', 'name': 'Dr. Reddy\'s Laboratories Limited',
                'price': Decimal('5500.00')},

            # Additional Indian Stocks - Infrastructure
            {'symbol': 'LT', 'name': 'Larsen & Toubro Limited',
                'price': Decimal('3200.00')},
            {'symbol': 'ADANIPORTS', 'name': 'Adani Ports and Special Economic Zone Limited',
                'price': Decimal('1200.00')},

            # Additional Indian Stocks - Energy
            {'symbol': 'ONGC', 'name': 'Oil and Natural Gas Corporation Limited',
                'price': Decimal('200.00')},
            {'symbol': 'NTPC', 'name': 'NTPC Limited',
                'price': Decimal('300.00')},

            # Additional Indian Stocks - Metals
            {'symbol': 'TATASTEEL', 'name': 'Tata Steel Limited',
                'price': Decimal('130.00')},
            {'symbol': 'JSWSTEEL', 'name': 'JSW Steel Limited',
                'price': Decimal('800.00')},

            # Additional US Stocks - Healthcare
            {'symbol': 'JNJ', 'name': 'Johnson & Johnson',
                'price': Decimal('158.00')},
            {'symbol': 'PFE', 'name': 'Pfizer Inc.',
                'price': Decimal('27.50')},
            {'symbol': 'UNH', 'name': 'UnitedHealth Group',
                'price': Decimal('490.00')},
            {'symbol': 'ABT', 'name': 'Abbott Laboratories',
                'price': Decimal('107.00')},

            # Additional US Stocks - Financial Services
            {'symbol': 'V', 'name': 'Visa Inc.',
                'price': Decimal('275.00')},
            {'symbol': 'MA', 'name': 'Mastercard Incorporated',
                'price': Decimal('470.00')},
            {'symbol': 'JPM', 'name': 'JPMorgan Chase & Co.',
                'price': Decimal('185.00')},
            {'symbol': 'BAC', 'name': 'Bank of America Corporation',
                'price': Decimal('35.00')},

            # Additional US Stocks - Technology & Communication
            # // Additional US Stocks
            {'symbol': 'PEP', 'name': 'PepsiCo, Inc.', 'price': Decimal('182.45')},
            {'symbol': 'KO', 'name': 'The Coca-Cola Company', 'price': Decimal('64.12')},
            {'symbol': 'WMT', 'name': 'Walmart Inc.', 'price': Decimal('154.33')},
            {'symbol': 'T', 'name': 'AT&T Inc.', 'price': Decimal('18.27')},
            {'symbol': 'VZ', 'name': 'Verizon Communications Inc.', 'price': Decimal('36.58')},
            {'symbol': 'CVX', 'name': 'Chevron Corporation', 'price': Decimal('165.89')},
            {'symbol': 'XOM', 'name': 'Exxon Mobil Corporation', 'price': Decimal('112.34')},
            {'symbol': 'PFE', 'name': 'Pfizer Inc.', 'price': Decimal('43.21')},
            {'symbol': 'MRK', 'name': 'Merck & Co., Inc.', 'price': Decimal('85.67')},
            {'symbol': 'ABBV', 'name': 'AbbVie Inc.', 'price': Decimal('120.45')},
            {'symbol': 'JNJ', 'name': 'Johnson & Johnson', 'price': Decimal('160.78')},
            {'symbol': 'UNH', 'name': 'UnitedHealth Group Incorporated', 'price': Decimal('510.23')},
            {'symbol': 'HD', 'name': 'The Home Depot, Inc.', 'price': Decimal('295.67')},
            {'symbol': 'LOW', 'name': 'Lowe\'s Companies, Inc.', 'price': Decimal('210.45')},
            {'symbol': 'UPS', 'name': 'United Parcel Service, Inc.', 'price': Decimal('180.56')},
            {'symbol': 'FDX', 'name': 'FedEx Corporation', 'price': Decimal('230.78')},
            {'symbol': 'BA', 'name': 'The Boeing Company', 'price': Decimal('220.34')},
            {'symbol': 'GE', 'name': 'General Electric Company', 'price': Decimal('105.89')},
            {'symbol': 'MMM', 'name': '3M Company', 'price': Decimal('98.45')},
            {'symbol': 'CAT', 'name': 'Caterpillar Inc.', 'price': Decimal('245.67')},
            {'symbol': 'DE', 'name': 'Deere & Company', 'price': Decimal('390.12')},
            {'symbol': 'GM', 'name': 'General Motors Company', 'price': Decimal('45.78')},
            {'symbol': 'F', 'name': 'Ford Motor Company', 'price': Decimal('12.34')},
            {'symbol': 'TSLA', 'name': 'Tesla, Inc.', 'price': Decimal('284.95')},
            {'symbol': 'AAPL', 'name': 'Apple Inc.', 'price': Decimal('209.28')},
            {'symbol': 'MSFT', 'name': 'Microsoft Corporation', 'price': Decimal('391.85')},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'price': Decimal('161.96')},
            {'symbol': 'AMZN', 'name': 'Amazon.com, Inc.', 'price': Decimal('188.99')},
            {'symbol': 'META', 'name': 'Meta Platforms, Inc.', 'price': Decimal('547.27')},
            {'symbol': 'NFLX', 'name': 'Netflix, Inc.', 'price': Decimal('628.00')},
            {'symbol': 'DIS', 'name': 'The Walt Disney Company', 'price': Decimal('112.00')},
            {'symbol': 'SBUX', 'name': 'Starbucks Corporation', 'price': Decimal('92.00')},
            {'symbol': 'NKE', 'name': 'NIKE, Inc.', 'price': Decimal('98.00')},
            {'symbol': 'MCD', 'name': 'McDonald\'s Corporation', 'price': Decimal('295.00')},
            {'symbol': 'V', 'name': 'Visa Inc.', 'price': Decimal('275.00')},
            {'symbol': 'MA', 'name': 'Mastercard Incorporated', 'price': Decimal('470.00')},
            {'symbol': 'PYPL', 'name': 'PayPal Holdings, Inc.', 'price': Decimal('62.00')},
            {'symbol': 'ADBE', 'name': 'Adobe Inc.', 'price': Decimal('485.00')},
            {'symbol': 'CRM', 'name': 'Salesforce, Inc.', 'price': Decimal('307.00')},
            {'symbol': 'INTC', 'name': 'Intel Corporation', 'price': Decimal('20.05')},
            {'symbol': 'NVDA', 'name': 'NVIDIA Corporation', 'price': Decimal('111.01')},
            {'symbol': 'CSCO', 'name': 'Cisco Systems, Inc.', 'price': Decimal('49.00')},
            {'symbol': 'ORCL', 'name': 'Oracle Corporation', 'price': Decimal('138.49')},
            {'symbol': 'IBM', 'name': 'International Business Machines Corporation', 'price': Decimal('232.41')},
            {'symbol': 'QCOM', 'name': 'QUALCOMM Incorporated', 'price': Decimal('167.00')},
            {'symbol': 'AMD', 'name': 'Advanced Micro Devices, Inc.', 'price': Decimal('178.00')},
            {'symbol': 'UBER', 'name': 'Uber Technologies, Inc.', 'price': Decimal('75.00')},
            {'symbol': 'LYFT', 'name': 'Lyft, Inc.', 'price': Decimal('14.67')},
            {'symbol': 'SNAP', 'name': 'Snap Inc.', 'price': Decimal('10.23')},
            {'symbol': 'TWTR', 'name': 'Twitter, Inc.', 'price': Decimal('54.20')},

            # Additional Indian Stocks
            {'symbol': 'RELIANCE', 'name': 'Reliance Industries Limited', 'price': Decimal('2800.00')},
            {'symbol': 'TCS', 'name': 'Tata Consultancy Services Limited', 'price': Decimal('3800.00')},
            {'symbol': 'INFY', 'name': 'Infosys Limited', 'price': Decimal('1500.00')},
            {'symbol': 'HDFCBANK', 'name': 'HDFC Bank Limited', 'price': Decimal('1500.00')},
            {'symbol': 'ICICIBANK', 'name': 'ICICI Bank Limited', 'price': Decimal('1000.00')},
            {'symbol': 'SBIN', 'name': 'State Bank of India', 'price': Decimal('600.00')},
            {'symbol': 'KOTAKBANK', 'name': 'Kotak Mahindra Bank Limited', 'price': Decimal('1700.00')},
            {'symbol': 'AXISBANK', 'name': 'Axis Bank Limited', 'price': Decimal('1000.00')},
            {'symbol': 'BAJFINANCE', 'name': 'Bajaj Finance Limited', 'price': Decimal('7000.00')},
            {'symbol': 'HINDUNILVR', 'name': 'Hindustan Unilever Limited', 'price': Decimal('2500.00')},
            # // Add more stocks as needed
        ]

        for stock_data in stocks:
            stock, created = Stock.objects.get_or_create(
                symbol=stock_data['symbol'],
                defaults={'name': stock_data['name'], 'price': stock_data['price']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added stock: {stock.symbol}"))
            else:
                self.stdout.write(self.style.WARNING(f"Stock already exists: {stock.symbol}"))

        self.stdout.write(self.style.SUCCESS('Successfully populated stocks'))
