from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ai_engine.services import stepfun
import json

PROMPTS = {
"india": """Generate TODAY's top India agriculture news digest. Be specific with real events, policies, prices.

TODAY'S INDIA AGRI NEWS

HEADLINE STORIES:
1. [Headline] | [Date context]
   [3-sentence detailed summary with specific numbers/names]

2. [Headline] | [Date context]
   [3-sentence summary]

3. [Headline] | [Date context]
   [3-sentence summary]

MSP & POLICY UPDATE:
[Latest MSP rates or government scheme update with specific numbers]

CROP PRICE FLASH:
Wheat: Rs.[price]/quintal ([change])
Rice: Rs.[price]/quintal ([change])
Soybean: Rs.[price]/quintal ([change])
Cotton: Rs.[price]/quintal ([change])
Onion: Rs.[price]/kg ([change])
Tomato: Rs.[price]/kg ([change])

WEATHER IMPACT:
[How current weather is affecting crops across India this week]

FARMER ALERT:
[Any urgent advisory — pest outbreak, extreme weather, scheme deadline]""",

"global": """Generate TODAY's top global agriculture news relevant to Indian farmers.

GLOBAL AGRI NEWS TODAY

INTERNATIONAL STORIES:
1. [Country/Region] — [Headline]
   [3-sentence summary with India impact]

2. [Country/Region] — [Headline]
   [3-sentence summary]

3. [Country/Region] — [Headline]
   [3-sentence summary]

GLOBAL COMMODITY PRICES:
Wheat (Chicago): $[price]/bushel ([change])
Rice (Bangkok): $[price]/ton ([change])
Soybean (Chicago): $[price]/bushel ([change])
Palm Oil (Malaysia): $[price]/ton ([change])
Sugar (NY): $[price]/lb ([change])

EXPORT/IMPORT NEWS:
[India export/import updates affecting farmers]

CLIMATE & FOOD SECURITY:
[Global climate news affecting agriculture]

IMPACT ON INDIAN FARMERS:
[How global events will affect Indian crop prices and exports]""",

"market": """Generate today's comprehensive Indian agricultural market price report.

MANDI PRICE REPORT — TODAY

MAJOR CROP PRICES (Rs. per quintal unless noted):

CEREALS:
Wheat: Rs.[price] | Change: [+/-X%] | Trend: [↑↓→]
Rice (Common): Rs.[price] | Change: [+/-X%]
Maize: Rs.[price] | Change: [+/-X%]
Jowar: Rs.[price] | Change: [+/-X%]
Bajra: Rs.[price] | Change: [+/-X%]

PULSES:
Tur Dal: Rs.[price] | Change: [+/-X%]
Chana: Rs.[price] | Change: [+/-X%]
Moong: Rs.[price] | Change: [+/-X%]
Urad: Rs.[price] | Change: [+/-X%]

OILSEEDS:
Soybean: Rs.[price] | Change: [+/-X%]
Groundnut: Rs.[price] | Change: [+/-X%]
Mustard: Rs.[price] | Change: [+/-X%]
Sunflower: Rs.[price] | Change: [+/-X%]

VEGETABLES (Rs./kg):
Onion: Rs.[price] | Tomato: Rs.[price] | Potato: Rs.[price]

CASH CROPS:
Cotton (per quintal): Rs.[price]
Sugarcane (per ton): Rs.[price]
Turmeric: Rs.[price]

TOP MANDI ACTIVITY TODAY:
1. [Mandi name, state] — [crop] — Rs.[price]
2. [Mandi name, state] — [crop] — Rs.[price]
3. [Mandi name, state] — [crop] — Rs.[price]

MARKET OUTLOOK:
[2-3 sentences on overall market trend this week]""",

"tips": """Generate practical farming tips and government scheme updates for Indian farmers today.

FARMER KNOWLEDGE HUB — TODAY

TECHNIQUE OF THE DAY:
Topic: [specific farming technique]
[4-5 sentences explaining the technique with practical steps]

GOVERNMENT SCHEMES UPDATE:
Scheme 1: [Name]
- Benefit: [what farmers get]
- Eligibility: [who can apply]
- How to apply: [specific steps]
- Deadline: [if any]

SEASONAL ADVISORY — [Current Month]:
[What farmers across India should be doing right now]

SOIL HEALTH TIP:
[Specific advice for maintaining/improving soil health]

WATER CONSERVATION TIP:
[Practical water-saving technique for this season]

PEST ALERT:
[Current pest or disease threat in India with identification and control]

SUCCESS STORY:
[Brief story of an Indian farmer using modern/organic techniques successfully]

DID YOU KNOW:
[Interesting agriculture fact relevant to Indian farming]"""
}

@login_required
def news(request):
    if request.method == "POST":
        try:
            d = json.loads(request.body)
            category = d.get("category","india")
            prompt = PROMPTS.get(category, PROMPTS["india"])
            result = stepfun([{"role":"user","content":prompt}], max_tokens=3000)
            return JsonResponse({"success": True, "result": result["content"]})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return render(request, "news/news.html")
