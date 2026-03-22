import requests, base64
from django.conf import settings

def _h():
    return {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

def stepfun(messages, system=None, max_tokens=3000):
    if system:
        system = system + "\n\nIMPORTANT: Always give complete, detailed responses. Never cut off mid-sentence. Cover every section fully."
    msgs = ([{"role":"system","content":system}] if system else []) + list(messages)
    try:
        r = requests.post(
            f"{settings.OPENROUTER_BASE_URL}/chat/completions",
            json={"model":settings.STEPFUN_MODEL,"messages":msgs,
                  "max_tokens":max_tokens,"reasoning":{"enabled":True}},
            headers=_h(), timeout=60)
        r.raise_for_status()
        d = r.json()
        if "error" in d:
            raise Exception(d["error"].get("message", str(d["error"])))
        m = d["choices"][0]["message"]
        return {"content": m.get("content",""), "reasoning": m.get("reasoning","")}
    except requests.exceptions.Timeout:
        raise Exception("Request timed out. Please try again.")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"API error {e.response.status_code}: {e.response.text[:300]}")

def gemini_vision(image_bytes, mime_type, prompt):
    b64 = base64.b64encode(image_bytes).decode()
    r = requests.post(
        f"{settings.OPENROUTER_BASE_URL}/chat/completions",
        json={"model":settings.GEMINI_MODEL,"max_tokens":1200,
              "messages":[{"role":"user","content":[
                  {"type":"image_url","image_url":{"url":f"data:{mime_type};base64,{b64}"}},
                  {"type":"text","text":prompt}
              ]}]},
        headers=_h(), timeout=90)
    r.raise_for_status()
    d = r.json()
    if "error" in d:
        raise Exception(d["error"].get("message", str(d["error"])))
    return d["choices"][0]["message"]["content"]

def open_meteo(lat, lon):
    """Free real-time weather from Open-Meteo — no API key needed."""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat, "longitude": lon,
            "current": ["temperature_2m","relative_humidity_2m","precipitation",
                        "wind_speed_10m","weather_code","apparent_temperature"],
            "daily": ["temperature_2m_max","temperature_2m_min","precipitation_sum",
                      "wind_speed_10m_max","weather_code"],
            "timezone": "Asia/Kolkata",
            "forecast_days": 7
        }
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return None

def geocode(location):
    """Geocode location name to lat/lon using Open-Meteo geocoding."""
    try:
        r = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 1, "language": "en"},
            timeout=8)
        r.raise_for_status()
        d = r.json()
        if d.get("results"):
            res = d["results"][0]
            return res["latitude"], res["longitude"], res.get("name",""), res.get("country","")
        return None
    except:
        return None
