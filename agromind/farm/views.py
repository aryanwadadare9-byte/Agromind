from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Farm, Crop, Activity, Harvest, Sale
import json


@login_required
def farm_home(request):
    try:
        farm = request.user.farm
    except Farm.DoesNotExist:
        return redirect("farm_setup")
    crops = farm.crops.all()
    activities = farm.activities.all()[:10]
    return render(request, "farm/farm.html", {
        "farm": farm,
        "crops": crops,
        "activities": activities,
        "growing_count": crops.filter(status="growing").count(),
        "harvested_count": crops.filter(status="harvested").count(),
        "planned_count": crops.filter(status="planned").count(),
        "total_cost": sum(float(c.act_cost) for c in crops),
        "total_revenue": sum(float(c.total_revenue) for c in crops),
        "profit": sum(c.profit for c in crops),
    })


@login_required
def farm_setup(request):
    farm = getattr(request.user, "farm", None)
    if request.method == "POST":
        d = request.POST
        if farm:
            farm.name = d["name"]
            farm.location = d["location"]
            farm.state = d.get("state", "Maharashtra")
            farm.area_acres = d["area_acres"]
            farm.soil_type = d["soil_type"]
            farm.irrigation = d.get("irrigation", "")
            farm.save()
        else:
            Farm.objects.create(
                user=request.user,
                name=d["name"],
                location=d["location"],
                state=d.get("state", "Maharashtra"),
                area_acres=d["area_acres"],
                soil_type=d["soil_type"],
                irrigation=d.get("irrigation", ""),
            )
        return redirect("farm")
    return render(request, "farm/setup.html", {"farm": farm})


@login_required
def add_crop(request):
    if request.method == "POST":
        d = request.POST
        farm = request.user.farm
        Crop.objects.create(
            farm=farm,
            name=d["name"],
            variety=d.get("variety", ""),
            season=d["season"],
            area_acres=d.get("area_acres") or 0,
            status=d.get("status", "planned"),
            exp_yield_kg=d.get("exp_yield_kg") or 0,
            exp_cost=d.get("exp_cost") or 0,
            sowing_date=d.get("sowing_date") or None,
            harvest_date=d.get("harvest_date") or None,
            notes=d.get("notes", ""),
        )
    return redirect("farm")


@login_required
def delete_crop(request, pk):
    get_object_or_404(Crop, pk=pk, farm__user=request.user).delete()
    return redirect("farm")


@login_required
def add_activity(request):
    if request.method == "POST":
        d = request.POST
        farm = request.user.farm
        cid = d.get("crop_id")
        crop = Crop.objects.filter(id=cid, farm=farm).first() if cid else None
        Activity.objects.create(
            farm=farm,
            crop=crop,
            activity_type=d.get("activity_type", "other"),
            cost=d.get("cost") or 0,
            date=d["date"],
            notes=d.get("notes", ""),
        )
    return redirect("farm")


@login_required
def delete_activity(request, pk):
    act = get_object_or_404(Activity, pk=pk, farm__user=request.user)
    # Reverse the cost from crop
    if act.crop:
        act.crop.act_cost = max(0, float(act.crop.act_cost) - float(act.cost))
        act.crop.save()
    act.delete()
    return redirect("farm")


@login_required
def add_harvest(request):
    if request.method == "POST":
        d = request.POST
        crop = get_object_or_404(Crop, id=d["crop_id"], farm__user=request.user)
        Harvest.objects.create(
            crop=crop,
            actual_yield_kg=d["actual_yield_kg"],
            harvest_date=d["harvest_date"],
            quality_grade=d.get("quality_grade", ""),
            notes=d.get("notes", ""),
        )
    return redirect("farm")


@login_required
def add_sale(request):
    if request.method == "POST":
        d = request.POST
        crop = get_object_or_404(Crop, id=d["crop_id"], farm__user=request.user)
        Sale.objects.create(
            crop=crop,
            quantity_kg=d["quantity_kg"],
            price_per_kg=d["price_per_kg"],
            buyer_name=d.get("buyer_name", ""),
            date=d["date"],
            notes=d.get("notes", ""),
        )
    return redirect("farm")