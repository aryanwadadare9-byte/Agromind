from django.db import models
from django.contrib.auth.models import User
class Detection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="disease/")
    crop_name = models.CharField(max_length=100, blank=True)
    result = models.TextField()
    disease_name = models.CharField(max_length=200, blank=True)
    severity = models.CharField(max_length=20, blank=True)
    confidence = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
