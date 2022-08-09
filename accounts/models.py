from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    cash = models.FloatField(default=10000, validators=[MaxValueValidator(1000000000), MinValueValidator(50)])
    # puchases = models.ManyToMany(Purchase, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def deposit(self, amount):
        self.cash = self.cash + amount

    def withdraw(self, amount):
        self.cash = self.cash - amount
    
    def can_purchase(self, amount):
        if amount <= self.cash:
            return True
        return False

class Purchase (models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    quantity = models.PositiveIntegerField(blank=False)
    original_price = models.FloatField()
    price_now = models.FloatField()
    purchase_time = models.DateTimeField(default=timezone.now)