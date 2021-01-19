from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    def __str__(self):
        return f"{self.username}"

class Listings(models.Model):
    title = models.CharField(max_length=180)
    description = models.CharField(max_length=300)
    price = models.FloatField()
    img_url = models.CharField(blank=True, max_length=300)
    category = models.CharField(blank=True, max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Item: {self.title} Price: {self.price} Category: {self.category}"


class Bid(models.Model):
    value = models.FloatField()
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")

    def __str__(self):
        return f"Bid: ${self.value} by {self.bidder}"
    

class Comment(models.Model):
    text = models.CharField(blank=True, max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="item")

    def __str__(self):
        return f"{self.author} commented {self.text} in {self.listing}"