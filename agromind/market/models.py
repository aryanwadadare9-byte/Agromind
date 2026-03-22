from django.db import models
from django.contrib.auth.models import User
class MarketQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
