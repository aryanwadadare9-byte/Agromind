from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ai_engine.services import stepfun
import json

@login_required
def organic(request):
    if request.method == "POST":
        try:
            d = json.loads(request.body)
            crop = d.get("crop","")
            problem = d.get("problem","")
            prompt = f"""You are an expert in organic and natural farming for Indian conditions.
Crop: {crop}
Problem / Goal: {problem}

Provide a complete organic solution:

DIAGNOSIS: [what is happening and why]

PRIMARY SOLUTION: [main organic method name]

INGREDIENTS:
- [Item]: [quantity for 1 acre] - [available at: local market/farm itself]
- [Item]: [quantity for 1 acre] - [available at]

PREPARATION STEPS:
Step 1: [detail]
Step 2: [detail]
Step 3: [detail]

APPLICATION:
Method: [how to apply]
Timing: [when - morning/evening, which stage of crop]
Dosage: [amount per acre or per litre water]
Frequency: [every X days]

RESULTS TIMELINE:
- Week 1: [what to expect]
- Week 2-3: [what to expect]
- Month 1: [final result]

COST ESTIMATE: Rs.[amount] per acre (vs chemical: Rs.[amount])

BONUS TIPS:
- [Extra tip 1]
- [Extra tip 2]

Use only locally available, affordable Indian materials."""
            result = stepfun([{"role":"user","content":prompt}], max_tokens=3000)
            return JsonResponse({"success": True, "result": result["content"], "reasoning": result.get("reasoning","")})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return render(request, "organic/organic.html")
