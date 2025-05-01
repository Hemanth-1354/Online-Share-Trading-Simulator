from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import CASCADE

# Profile model to hold additional user data like balance


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_pin = models.CharField(
        max_length=6, default='000000')  # Default PIN is 000000

    def __str__(self):
        return f"{self.user.username}'s Profile"

    # Helper method to get stock holdings for the user
    def get_stock_holdings(self):
        return self.stock_holdings.all()


# Transaction model to hold buy/sell transactions
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_name = models.CharField(max_length=100, default='Unknown Stock')
    stock_symbol = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(
        choices=[('BUY', 'Buy'), ('SELL', 'Sell')], max_length=4)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} {self.transaction_type} {self.quantity} {self.stock_name}"


# Stock model to represent stocks being traded
class Stock(models.Model):
    # Stock symbol like 'AAPL', 'GOOG', etc.
    symbol = models.CharField(max_length=10, unique=True)
    # Stock full name, e.g., 'Apple Inc.'
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Stock price
    # Timestamp for the last time the price was updated
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"


# StockHolding model to represent the relationship between Profile and Stock
class StockHolding(models.Model):
    # ForeignKey to Profile (the user who owns the stocks)
    profile = models.ForeignKey(
        Profile, on_delete=CASCADE, related_name='stock_holdings')

    # ForeignKey to Stock (the actual stock being held)
    stock = models.ForeignKey(Stock, on_delete=CASCADE,
                              related_name='stock_holdings')

    # The quantity of stocks owned by the user
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.profile.user.username} holds {self.quantity} of {self.stock.name} ({self.stock.symbol})"


# Signal to create or update user profile when a new user is created or updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Avoid circular imports by importing Profile inside the function
    if created:
        # Create a new Profile with the initial balance when a user is created
        Profile.objects.create(user=instance)
    # Ensure the profile is saved if any changes happen to the user
    instance.profile.save()
