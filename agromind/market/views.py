from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import MarketQuery
from ai_engine.services import stepfun
import json

@login_required
def market(request):
    if request.method == "POST":
        try:
            d = json.loads(request.body)
            crop = d.get("crop", "")
            location = d.get("location", "")
            season = d.get("season", "")
            prompt = f"""You are an expert Indian agricultural market analyst.
Crop: {crop} | Location/Mandi: {location} | Season: {season}

Give a complete structured market analysis:

CURRENT_PRICE: Rs.[min]-[max] per quintal
RECOMMENDED_PRICE: Rs.[amount] per quintal
TREND: [Rising/Falling/Stable]
TREND_REASON: [1 sentence why]
DEMAND: [High/Medium/Low]
BEST_SELL_TIME: [specific period]

TOP MANDIS:
1. [Mandi name, state] - Rs.[price]/quintal
2. [Mandi name, state] - Rs.[price]/quintal
3. [Mandi name, state] - Rs.[price]/quintal

PRICE FACTORS:
- [Factor 1 with impact]
- [Factor 2 with impact]
- [Factor 3 with impact]

6-MONTH FORECAST:
Month 1 ([name]): Rs.[range]
Month 2 ([name]): Rs.[range]
Month 3 ([name]): Rs.[range]
Month 4 ([name]): Rs.[range]
Month 5 ([name]): Rs.[range]
Month 6 ([name]): Rs.[range]

GOVERNMENT MSP: Rs.[amount] per quintal (if applicable)

RECOMMENDATION:
[2-3 sentences of specific actionable advice for the farmer]

Use real Indian market data and current prices."""
            result = stepfun([{"role":"user","content":prompt}], max_tokens=3000)
            MarketQuery.objects.create(user=request.user, crop=crop, location=location, result=result["content"])
            return JsonResponse({"success": True, "result": result["content"], "reasoning": result.get("reasoning","")})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    recent = MarketQuery.objects.filter(user=request.user)[:5]
    return render(request, "market/market.html", {"recent": recent})
