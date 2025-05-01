from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('transaction-history/', views.transaction_history,
         name='transaction_history'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('add-money/', views.add_money, name='add_money'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('news/', views.news_view, name='news'),
    # Adjusted to match the function name in views.py
    path('fetch-stock-price/', views.ajax_fetch_stock_price,
         name='fetch_stock_price'),
    path('search-stocks/', views.search_stocks, name='search_stocks'),
    path('admin/users/', views.admin_user_list, name='admin_user_list'),
    path('admin/transactions/', views.admin_transaction_list, name='admin_transaction_list'),
]
