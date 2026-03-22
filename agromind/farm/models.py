from django.db import models
from django.contrib.auth.models import User


class Farm(models.Model):
    SOIL = [
        ("black", "Black Cotton"), ("red", "Red Laterite"),
        ("alluvial", "Alluvial"), ("sandy", "Sandy Loam"), ("clay", "Clay")
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="farm")
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    state = models.CharField(max_length=100, default="Maharashtra")
    area_acres = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    soil_type = models.CharField(max_length=20, choices=SOIL, default="black")
    irrigation = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Crop(models.Model):
    SEASON = [
        ("kharif", "Kharif"), ("rabi", "Rabi"), ("zaid", "Zaid")
    ]
    STATUS = [
        ("planned", "Planned"), ("growing", "Growing"), ("harvested", "Harvested")
    ]
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="crops")
    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100, blank=True)
    season = models.CharField(max_length=10, choices=SEASON)
    area_acres = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    status = models.CharField(max_length=15, choices=STATUS, default="planned")
    exp_yield_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    act_yield_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    exp_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    act_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sowing_date = models.DateField(null=True, blank=True)
    harvest_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.farm.name})"

    @property
    def profit(self):
        return float(self.total_revenue) - float(self.act_cost)


class Activity(models.Model):
    TYPES = [
        ("seed", "Seed Purchase"),
        ("fertilizer", "Fertilizer"),
        ("irrigation", "Irrigation"),
        ("labor", "Labor"),
        ("pesticide", "Pesticide"),
        ("harvesting", "Harvesting"),
        ("ploughing", "Ploughing"),
        ("other", "Other"),
    ]
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="activities")
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True, related_name="activities")
    activity_type = models.CharField(max_length=20, choices=TYPES)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        # If editing existing, reverse old cost first
        if self.pk:
            old = Activity.objects.get(pk=self.pk)
            if old.crop:
                old.crop.act_cost = max(0, float(old.crop.act_cost) - float(old.cost))
                old.crop.save()
        super().save(*args, **kwargs)
        # Add new cost to crop
        if self.crop:
            self.crop.act_cost = float(self.crop.act_cost) + float(self.cost)
            self.crop.save()


class Harvest(models.Model):
    GRADE = [("A", "Grade A"), ("B", "Grade B"), ("C", "Grade C")]
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="harvests")
    actual_yield_kg = models.DecimalField(max_digits=10, decimal_places=2)
    harvest_date = models.DateField()
    quality_grade = models.CharField(max_length=1, choices=GRADE, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-harvest_date"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update crop actual yield and status
        total = sum(float(h.actual_yield_kg) for h in self.crop.harvests.all())
        self.crop.act_yield_kg = total
        self.crop.status = "harvested"
        self.crop.harvest_date = self.harvest_date
        self.crop.save()


class Sale(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="sales")
    quantity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    buyer_name = models.CharField(max_length=200, blank=True)
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        # Auto calculate revenue
        self.revenue = float(self.quantity_kg) * float(self.price_per_kg)
        super().save(*args, **kwargs)
        # Update crop total revenue
        total = sum(float(s.revenue) for s in self.crop.sales.all())
        self.crop.total_revenue = total
        self.crop.save()