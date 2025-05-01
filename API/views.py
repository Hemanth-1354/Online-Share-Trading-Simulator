from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.http import JsonResponse
from django.core.cache import cache
import time
import requests
from .models import Profile, Transaction, StockHolding, Stock
from .forms import StockSearchForm
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import CASCADE
from decimal import Decimal, InvalidOperation  # Update this line
import random
import re  # Add this import
from django.db.models import Q
from django.core.exceptions import ValidationError
import json
from django.db.models import Sum
from django.utils import timezone
from django.db import transaction
import os
import requests
from django.contrib.auth.decorators import login_required
from .models import User, Transaction

@login_required(login_url='login')
def news_view(request):
    try:
        api_key = os.getenv('FINNHUB_API_KEY')
        print(f"DEBUG: API Key value: {api_key}")  # Debug API key value
        
        if not api_key:
            messages.error(request, 'Finnhub API key not found in environment variables')
            return render(request, 'news.html', {'news_items': []})

        url = 'https://finnhub.io/api/v1/news'
        params = {
            'token': api_key,
            'category': 'general',  # Can be: general, forex, crypto, merger
            'minId': 0
        }
        
        print("DEBUG: Making API request to:", url)
        print("DEBUG: Parameters:", params)
        
        response = requests.get(url, params=params)
        print(f"DEBUG: Response Status Code: {response.status_code}")
        print(f"DEBUG: Response Content: {response.text[:500]}")  # Print first 500 chars of response
        
        if response.status_code == 200:
            news_data = response.json()
            # Transform Finnhub response to match our template format
            news_items = [{
                'title': item.get('headline', ''),
                'description': item.get('summary', ''),
                'url': item.get('url', ''),
                'urlToImage': item.get('image', ''),
                'source': {'name': item.get('source', 'Finnhub')},
                'publishedAt': item.get('datetime', '')
            } for item in news_data[:12]]  # Limit to 12 items
            
            if not news_items:
                print("DEBUG: No news items found in response")
            return render(request, 'news.html', {'news_items': news_items})
        elif response.status_code == 401:
            messages.error(request, 'Invalid API key. Please check your Finnhub API configuration.')
            print("DEBUG: API Authentication failed")
        elif response.status_code == 429:
            messages.error(request, 'API request limit reached. Please try again later.')
            print("DEBUG: API rate limit exceeded")
        else:
            messages.error(request, f'Unable to fetch news. Status code: {response.status_code}')
            print(f"DEBUG: Unexpected status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"DEBUG: Request Exception: {str(e)}")
        messages.error(request, 'Network error while fetching news')
    except json.JSONDecodeError as e:
        print(f"DEBUG: JSON Decode Error: {str(e)}")
        messages.error(request, 'Error parsing news data')
    except Exception as e:
        print(f"DEBUG: Unexpected Error: {str(e)}")
        messages.error(request, 'An unexpected error occurred')
    
    return render(request, 'news.html', {'news_items': []})

# Home page


def index(request):
    return render(request, 'index.html')

# Login view


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')

# Signup view


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists.')
                return render(request, 'signup.html', {'form': form})
            try:
                user = form.save()
                login(request, user)
                return redirect('dashboard')
            except IntegrityError:
                form.add_error(None, 'Error creating account.')
        return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

# Logout view


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('home')

# Transaction history view


@login_required(login_url='login')
def transaction_history(request):
    transaction_type = request.GET.get('type', 'all')
    
    transactions = Transaction.objects.filter(user=request.user)
    
    if transaction_type == 'withdrawal':
        transactions = transactions.filter(transaction_type='WITHDRAW')  # Changed to match the type used in withdraw_view
    elif transaction_type == 'deposit':
        transactions = transactions.filter(transaction_type='DEPOSIT')
    elif transaction_type == 'buy':
        transactions = transactions.filter(transaction_type='BUY')
    elif transaction_type == 'sell':
        transactions = transactions.filter(transaction_type='SELL')
    
    transactions = transactions.order_by('-date')
    
    return render(request, 'transaction_history.html', {
        'transactions': transactions,
        'current_filter': transaction_type
    })


# Stock API URL and headers for fetching stock prices
STOCK_API_URL = 'https://yh-finance.p.rapidapi.com/stock/v2/get-summary'
API_HEADERS = {
    'X-RapidAPI-Host': 'yh-finance.p.rapidapi.com',
    'X-RapidAPI-Key': settings.RAPIDAPI_KEY,
}

# Function to fetch stock price using the Yahoo Finance API


def fetch_stock_price(symbol):
    # Check if the price is cached
    cached_price = cache.get(symbol)
    if cached_price:
        return cached_price  # Return cached price if available

    # If not cached, fetch data from the API
    try:
        url = f'{STOCK_API_URL}'
        params = {'symbol': symbol}

        # Add a delay to avoid hitting the API rate limit
        time.sleep(1)

        response = requests.get(url, headers=API_HEADERS, params=params)

        if response.status_code == 429:  # Rate Limit Exceeded
            time.sleep(60)  # Wait for 60 seconds before retrying
            return fetch_stock_price(symbol)  # Retry the request

        response.raise_for_status()  # Raise an exception for any non-2xx response
        data = response.json()

        # Check if 'financialData' is in the response
        if 'financialData' in data:
            price = data['financialData']['currentPrice']['raw']
            # Cache the result for 5 minutes
            cache.set(symbol, price, timeout=300)
            return price
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

# Helper function to fetch stock data (if required)


def get_stock_data_from_api(symbol):
    try:
        # Convert symbol to uppercase for case-insensitive search
        search_term = symbol.upper()
        print(f"Searching for stock with term: {search_term}")

        # Try to get the stock from our database by symbol or name
        stock = Stock.objects.filter(
            Q(symbol__iexact=search_term) |
            Q(name__icontains=search_term)
        ).first()

        if not stock:
            print(f"Stock not found in database: {search_term}")
            # List available stocks for debugging
            available_stocks = Stock.objects.values_list('symbol', flat=True)
            print(f"Available stocks: {list(available_stocks)}")
            return None

        print(f"Found stock: {stock.name} ({stock.symbol})")

        # Generate a more realistic price change
        # 60% chance of positive change, 40% chance of negative change
        if random.random() < 0.6:  # 60% chance of positive change
            change = Decimal(str(random.uniform(0.1, 3.0))
                             )  # 0.1% to 3% increase
        else:
            change = Decimal(str(random.uniform(-2.0, -0.1))
                             )  # -2% to -0.1% decrease

        print(f"Generated price change: {change}%")

        # Update the price with the change
        new_price = stock.price * (Decimal('1') + change/Decimal('100'))
        print(f"New price: {new_price}")

        stock_data = {
            'symbol': stock.symbol,
            'name': stock.name,
            'price': round(new_price, 2),
            'change': float(round(change, 2))
        }

        print(f"Returning stock data: {stock_data}")
        return stock_data

    except Exception as e:
        print(f"Error fetching stock data: {str(e)}")
        return None

# Dashboard view to handle stock transactions


@login_required(login_url='login')
def dashboard_view(request):
    profile = request.user.profile
    stock_data = None

    # Handle stock search
    if request.method == 'POST' and 'search_name' in request.POST:
        symbol = request.POST.get('search_name').upper()
        stock_data = get_stock_data_from_api(symbol)
        if not stock_data:
            messages.error(
                request, f'Could not find stock with symbol {symbol}')

    # Handle buy/sell transaction
    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST.get('action')
        symbol = request.POST.get('symbol')
        quantity = int(request.POST.get('quantity'))
        price = Decimal(request.POST.get('price'))

        try:
            stock = Stock.objects.get(symbol=symbol)

            if action == 'buy':
                total_cost = price * quantity
                if profile.balance >= total_cost:
                    # Create or update stock holding
                    holding, created = StockHolding.objects.get_or_create(
                        profile=profile,
                        stock=stock,
                        defaults={'quantity': quantity}
                    )

                    if not created:
                        holding.quantity += quantity
                        holding.save()

                    # Create transaction record
                    Transaction.objects.create(
                        user=request.user,
                        stock_symbol=symbol,
                        stock_name=stock.name,
                        transaction_type='BUY',
                        quantity=quantity,
                        price=price
                    )

                    # Update profile balance
                    profile.balance -= total_cost
                    profile.save()

                    messages.success(
                        request, f'Successfully bought {quantity} shares of {symbol}')
                else:
                    messages.error(
                        request, 'Insufficient balance for this transaction')

            elif action == 'sell':
                # Check if user has enough shares to sell
                try:
                    holding = StockHolding.objects.get(
                        profile=profile, stock=stock)

                    if holding.quantity >= quantity:
                        # Update holding
                        holding.quantity -= quantity
                        if holding.quantity == 0:
                            holding.delete()
                        else:
                            holding.save()

                        # Create transaction record
                        Transaction.objects.create(
                            user=request.user,
                            stock_symbol=symbol,
                            stock_name=stock.name,
                            transaction_type='SELL',
                            quantity=quantity,
                            price=price
                        )

                        # Update profile balance
                        profile.balance += price * quantity
                        profile.save()

                        messages.success(
                            request, f'Successfully sold {quantity} shares of {symbol}')
                    else:
                        messages.error(request, 'Insufficient shares to sell')
                except StockHolding.DoesNotExist:
                    messages.error(
                        request, f'You do not own any shares of {symbol}')

            # Refresh stock data after transaction
            stock_data = get_stock_data_from_api(symbol)

        except Stock.DoesNotExist:
            messages.error(request, f'Stock {symbol} not found')
        except Exception as e:
            messages.error(request, f'Error processing transaction: {str(e)}')

    context = {
        'profile': profile,
        'stock_data': stock_data
    }

    return render(request, 'dashboard.html', context)


# Portfolio view to display user's stock holdings and balance


@login_required
def portfolio_view(request):
    profile = request.user.profile  # Get user's profile

    # Get the user's stock holdings from the StockHolding model
    stock_holdings = StockHolding.objects.filter(profile=profile)

    # Prepare data for portfolio display
    holdings = []
    total_investment = Decimal('0')
    total_current_value = Decimal('0')

    for holding in stock_holdings:
        stock = holding.stock
        current_value = holding.quantity * stock.price
        total_current_value += current_value

        # Calculate average purchase price from transactions
        buy_transactions = Transaction.objects.filter(
            user=request.user,
            stock_symbol=stock.symbol,
            transaction_type='BUY'
        )

        total_quantity = 0
        total_cost = Decimal('0')

        for transaction in buy_transactions:
            total_quantity += transaction.quantity
            total_cost += transaction.price * transaction.quantity

        if total_quantity > 0:
            avg_purchase_price = total_cost / total_quantity
            investment = avg_purchase_price * holding.quantity
            total_investment += investment
            profit = current_value - investment
            profit_percentage = (profit / investment *
                                 100) if investment > 0 else 0
        else:
            avg_purchase_price = Decimal('0')
            profit = Decimal('0')
            profit_percentage = Decimal('0')

        holdings.append({
            'stock': stock,
            'quantity': holding.quantity,
            'current_value': current_value,
            'avg_purchase_price': round(avg_purchase_price, 2),
            'profit': round(profit, 2),
            'profit_percentage': round(profit_percentage, 2)
        })

    # Calculate total profit/loss
    total_profit = total_current_value - total_investment
    total_profit_percentage = (
        total_profit / total_investment * 100) if total_investment > 0 else 0

    # Total portfolio value includes current value of stocks plus wallet balance
    total_portfolio_value = total_current_value

    context = {
        'profile': profile,
        'holdings': holdings,
        'total_profit': round(total_profit, 2),
        'total_investment': round(total_investment, 2),
        'total_portfolio_value': round(total_portfolio_value, 2),
        'total_profit_percentage': round(total_profit_percentage, 2)
    }

    return render(request, 'portfolio.html', context)

# AJAX View for Fetching Stock Price (AJAX Request)


@csrf_exempt
def ajax_fetch_stock_price(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        # Call the function to fetch the price
        price = fetch_stock_price(symbol)

        if price:
            return JsonResponse({'price': price})
        else:
            return JsonResponse({'error': 'Failed to fetch price for the symbol'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

# Add money to wallet view


@login_required(login_url='login')
def add_money(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount', '0'))
            if amount <= 0:
                messages.error(request, 'Please enter a valid amount.')
                return redirect('dashboard')

            profile = request.user.profile
            profile.balance += amount
            profile.save()

            # Create transaction record for deposit
            Transaction.objects.create(
                user=request.user,
                transaction_type='DEPOSIT',
                quantity=1,
                price=amount,
                stock_symbol='CASH',
                stock_name='Cash Deposit'
            )

            messages.success(request, f'Successfully added Rs. {amount:,.2f} to your account.')
        except (InvalidOperation, ValueError):
            messages.error(request, 'Please enter a valid amount.')
        except Exception as e:
            messages.error(request, 'An error occurred while processing your request.')
            print(f"Add money error: {str(e)}")

    return redirect('dashboard')

# Add this new view


def search_stocks(request):
    query = request.GET.get('query', '').strip()
    if len(query) < 2:
        return JsonResponse({'results': []})

    # Search in both symbol and name fields
    stocks = Stock.objects.filter(
        Q(symbol__icontains=query) |
        Q(name__icontains=query)
    )[:10]  # Limit to 10 results

    results = [
        {
            'symbol': stock.symbol,
            'name': stock.name,
            'price': float(stock.price)
        }
        for stock in stocks
    ]

    return JsonResponse({'results': results})

# Add the withdraw view


@login_required(login_url='login')
def withdraw_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        try:
            # Move all validations before the transaction block
            amount = Decimal(request.POST.get('amount', '0'))
            upi_id = request.POST.get('upi_id', '').strip()
            phone = request.POST.get('phone', '').strip()
            name = request.POST.get('name', '').strip()
            captcha = request.POST.get('captcha', '').strip()
            session_captcha = request.session.get('withdrawal_captcha', '')

            # Validate amount
            if amount <= 0:
                raise ValidationError('Please enter a valid withdrawal amount.')
                
            if amount < Decimal('2000'):
                raise ValidationError('Minimum withdrawal amount is Rs. 2,000.')

            if amount > profile.balance:
                raise ValidationError('Withdrawal amount cannot exceed your balance.')
            
            # Check daily withdrawal limit
            today = timezone.now().date()
            today_withdrawals = Transaction.objects.filter(
                user=request.user,
                transaction_type='WITHDRAW',
                date__date=today
            ).aggregate(total=Sum('price'))['total'] or Decimal('0')

            if today_withdrawals + amount > Decimal('150000'):
                raise ValidationError(
                    'Daily withdrawal limit of Rs. 1,50,000 exceeded. '
                    f'You have already withdrawn Rs. {today_withdrawals:,.2f} today.'
                )

            # Validate UPI ID
            if not upi_id or not re.match(r'^[a-zA-Z0-9.\-_]{3,}@[a-zA-Z][a-zA-Z]{2,}$', upi_id):
                raise ValidationError('Please enter a valid UPI ID (e.g., username@bankname)')

            # Validate Name and Phone

            if not name or not re.match(r'^[A-Za-z\s]{3,}$', name):
                raise ValidationError('Please enter a valid name (letters and spaces only).')


            if not phone or not phone.isdigit() or len(phone) != 10:
                raise ValidationError('Please enter a valid 10-digit phone number.')

            # Validate Captcha
            if not captcha or captcha != session_captcha:
                raise ValidationError('Invalid security code. Please try again.')

            # If all validations pass, process the withdrawal in a transaction block
            with transaction.atomic():
                try:
                    # Lock the profile row for update
                    profile = Profile.objects.select_for_update().get(id=profile.id)
                    
                    if profile.balance < amount:  # Double-check balance
                        raise ValidationError('Insufficient balance for withdrawal.')
                    
                    # Create transaction record first
                    withdrawal_transaction = Transaction.objects.create(
                        user=request.user,
                        transaction_type='WITHDRAW',
                        quantity=1,
                        price=amount,
                        stock_symbol='CASH',
                        stock_name='Cash Withdrawal'
                    )

                    # Update profile balance
                    profile.balance -= amount
                    profile.save()

                    # Create withdrawal transaction record
                    Transaction.objects.create(
                        user=request.user,
                        transaction_type='WITHDRAWAL',  # Changed from 'WITHDRAW' to 'WITHDRAWAL'
                        quantity=1,
                        price=amount,
                        stock_symbol='CASH',
                        stock_name='Cash Withdrawal'
                    )

                    messages.success(request, f'Successfully withdrawn Rs. {amount:,.2f}. It will be credited to your UPI ID {upi_id}')
                    return redirect('dashboard')

                except Profile.DoesNotExist:
                    raise ValidationError('User profile not found.')
                except IntegrityError:
                    raise ValidationError('Database error occurred. Please try again.')

        except ValidationError as e:
            messages.error(request, str(e))
        except InvalidOperation:
            messages.error(request, 'Please enter a valid amount.')
        except IntegrityError:
            messages.error(request, 'Transaction failed. Please try again.')
        except Exception as e:
            messages.error(request, 'An unexpected error occurred. Please try again.')
            print(f"Withdrawal error: {str(e)}")  # Log the error for debugging

    # Generate new captcha for the withdrawal form
    import random
    import string

    # Generate a random 6-character captcha with mixed case letters and numbers
    captcha_text = ''.join(random.choices(
        string.ascii_letters + string.digits,
        k=6
    ))
    request.session['withdrawal_captcha'] = captcha_text

    context = {
        'profile': profile,
        'daily_limit': Decimal('150000'),
        'today_withdrawals': Transaction.objects.filter(
            user=request.user,
            transaction_type='WITHDRAW',
            date__date=timezone.now().date()
        ).aggregate(total=Sum('price'))['total'] or Decimal('0'),
        'captcha_text': captcha_text,
        'form_data': request.POST if request.method == 'POST' else None
    }
    return render(request, 'withdraw.html', context)


def admin_user_list(request):
    users = User.objects.all()
    return render(request, 'admin_user_list.html', {'users': users})

def admin_transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'admin_transaction_list.html', {'transactions': transactions})
