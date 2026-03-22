# AgroMind — AI Agriculture Platform

## 7 Modules
1. Dashboard — charts, weather, AI daily plan
2. Farm Manager — crops, activities, profit tracking
3. Disease Detector — Gemini Vision AI image analysis
4. Market Prices — StepFun AI price prediction
5. Organic Guide — StepFun AI organic solutions
6. Rainfall & Weather — Open-Meteo real-time API + AI advisory
7. Agriculture News — StepFun AI India + Global news

## Setup
```bash
pip install -r requirements.txt

# Edit agro/settings.py:
# - Set PostgreSQL credentials
# - Set OPENROUTER_API_KEY (get from openrouter.ai)
# - Open-Meteo is FREE — no key needed

python manage.py makemigrations users farm disease market organic rainfall news dashboard ai_engine
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## APIs Used
- OpenRouter (openrouter.ai) — StepFun step-3.5-flash + Gemini Flash Vision
- Open-Meteo (open-meteo.com) — FREE real-time weather, no API key needed
