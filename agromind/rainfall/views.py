from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ai_engine.services import stepfun, open_meteo, geocode
import json

WMO_CODES = {
    0:"Clear sky", 1:"Mainly clear", 2:"Partly cloudy", 3:"Overcast",
    45:"Foggy", 48:"Icy fog", 51:"Light drizzle", 53:"Drizzle", 55:"Heavy drizzle",
    61:"Slight rain", 63:"Moderate rain", 65:"Heavy rain",
    71:"Slight snow", 73:"Moderate snow", 75:"Heavy snow",
    80:"Slight showers", 81:"Moderate showers", 82:"Violent showers",
    95:"Thunderstorm", 96:"Thunderstorm with hail", 99:"Heavy thunderstorm"
}

@login_required
def weather_api(request):
    location = request.GET.get("location", "")
    if not location:
        return JsonResponse({"success": False, "error": "No location provided"})
    geo = geocode(location)
    if not geo:
        return JsonResponse({"success": False, "error": "Location not found"})
    lat, lon, city, country = geo
    data = open_meteo(lat, lon)
    if not data:
        return JsonResponse({"success": False, "error": "Weather data unavailable"})
    cur = data.get("current", {})
    daily = data.get("daily", {})
    weather = {
        "city": city,
        "country": country,
        "lat": lat,
        "lon": lon,
        "temp": cur.get("temperature_2m"),
        "feels_like": cur.get("apparent_temperature"),
        "humidity": cur.get("relative_humidity_2m"),
        "wind": cur.get("wind_speed_10m"),
        "rain": cur.get("precipitation"),
        "description": WMO_CODES.get(cur.get("weather_code", 0), "Unknown"),
        "forecast": []
    }
    times = daily.get("time", [])
    for i in range(min(7, len(times))):
        weather["forecast"].append({
            "date": times[i],
            "max": daily.get("temperature_2m_max", [])[i] if i < len(daily.get("temperature_2m_max", [])) else None,
            "min": daily.get("temperature_2m_min", [])[i] if i < len(daily.get("temperature_2m_min", [])) else None,
            "rain": daily.get("precipitation_sum", [])[i] if i < len(daily.get("precipitation_sum", [])) else 0,
            "desc": WMO_CODES.get(daily.get("weather_code", [])[i] if i < len(daily.get("weather_code", [])) else 0, "")
        })
    return JsonResponse({"success": True, "weather": weather})

@login_required
def rainfall(request):
    if request.method == "POST":
        try:
            d = json.loads(request.body)
            location = d.get("location", "")
            crop = d.get("crop", "")
            month = d.get("month", "")

            geo = geocode(location)
            weather_ctx = ""
            forecast_ctx = ""

            if geo:
                lat, lon, city, country = geo
                data = open_meteo(lat, lon)
                if data:
                    cur = data.get("current", {})
                    daily = data.get("daily", {})
                    temp = cur.get("temperature_2m")
                    feels = cur.get("apparent_temperature")
                    humidity = cur.get("relative_humidity_2m")
                    rain = cur.get("precipitation")
                    wind = cur.get("wind_speed_10m")
                    desc = WMO_CODES.get(cur.get("weather_code", 0), "Unknown")
                    weather_ctx = (
                        "REAL-TIME WEATHER DATA for " + city + ", " + country + ":\n"
                        "Temperature: " + str(temp) + "C (feels like " + str(feels) + "C)\n"
                        "Humidity: " + str(humidity) + "%\n"
                        "Current Precipitation: " + str(rain) + " mm\n"
                        "Wind Speed: " + str(wind) + " km/h\n"
                        "Conditions: " + desc
                    )
                    times = daily.get("time", [])
                    rain_vals = daily.get("precipitation_sum", [])
                    forecast_lines = ["7-DAY FORECAST:"]
                    for i in range(min(7, len(times))):
                        r = rain_vals[i] if i < len(rain_vals) else 0
                        forecast_lines.append("  " + times[i] + ": " + str(r) + " mm rain")
                    forecast_ctx = "\n".join(forecast_lines)

            prompt = (
                "You are an expert agricultural meteorologist for India.\n"
                "Location: " + location + " | Crop: " + crop + " | Month: " + month + "\n"
                + weather_ctx + "\n"
                + forecast_ctx + "\n\n"
                "Using the real-time data above, provide:\n\n"
                "WEATHER SUMMARY:\n"
                "[Describe current conditions and what they mean for farming]\n\n"
                "RAINFALL ANALYSIS FOR " + month.upper() + ":\n"
                "Expected Total Rainfall: [X mm]\n"
                "Compared to Normal: [Above/Below/Normal by X%]\n"
                "Distribution: [Early/Mid/Late month heavy]\n"
                "Confidence: [%]\n\n"
                "RISK ASSESSMENT:\n"
                "Drought Risk: [Low/Medium/High] - [reason]\n"
                "Flood Risk: [Low/Medium/High] - [reason]\n"
                "Crop Loss Risk: [Low/Medium/High] - [reason]\n\n"
                "IRRIGATION PLAN FOR " + crop.upper() + ":\n"
                "Current Water Need: [litres/day per acre]\n"
                "Recommended Schedule: [specific days and amounts]\n"
                "Method: [drip/sprinkler/flood]\n"
                "Water Saving Tips: [specific advice]\n\n"
                "FARMING ACTIONS FOR " + month.upper() + ":\n"
                "1. [Urgent action based on forecast]\n"
                "2. [Crop-specific action]\n"
                "3. [Soil management]\n"
                "4. [Pest/disease risk from this weather]\n\n"
                "7-DAY OUTLOOK:\n"
                "[Day by day brief advisory based on the real forecast data above]\n\n"
                "CLIMATE ADVISORY:\n"
                "[Long-term seasonal outlook for this region]"
            )

            result = stepfun([{"role": "user", "content": prompt}], max_tokens=3000)
            return JsonResponse({
                "success": True,
                "result": result["content"],
                "reasoning": result.get("reasoning", "")
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return render(request, "rainfall/rainfall.html")