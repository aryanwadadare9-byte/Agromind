from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Detection
from ai_engine.services import gemini_vision

PROMPT = """You are an expert plant pathologist. Analyze this crop image and respond in EXACTLY this format:

DISEASE_NAME: [name or Healthy]
SEVERITY: [Mild/Moderate/Severe/Healthy]
CONFIDENCE: [number]%
AFFECTED_PART: [leaf/stem/root/fruit/whole plant]
CAUSE: [Fungal/Bacterial/Viral/Pest/Nutrient Deficiency/Healthy]

SYMPTOMS:
[what you observe in the image - 2-3 sentences]

CHEMICAL_TREATMENT:
Product: [specific product name]
Dosage: [amount per litre/acre]
Frequency: [how often]

ORGANIC_TREATMENT:
[specific organic remedy with preparation and application]

PREVENTION:
1. [tip 1]
2. [tip 2]
3. [tip 3]

URGENCY: [Immediate Action/Within a Week/Monitor/No Action Needed]

Be specific and practical for Indian farmers."""

def _get(text, key):
    for line in text.split("\n"):
        if line.startswith(key + ":"):
            return line.split(":", 1)[1].strip()
    return ""

@login_required
def detect(request):
    if request.method == "POST" and request.FILES.get("image"):
        img = request.FILES["image"]
        crop_name = request.POST.get("crop_name", "")
        try:
            result = gemini_vision(img.read(), img.content_type, PROMPT)
            det = Detection.objects.create(
                user=request.user, image=img, crop_name=crop_name,
                result=result,
                disease_name=_get(result, "DISEASE_NAME"),
                severity=_get(result, "SEVERITY"),
                confidence=_get(result, "CONFIDENCE"),
            )
            return JsonResponse({"success": True, "result": result,
                "disease": det.disease_name, "severity": det.severity,
                "confidence": det.confidence, "image_url": det.image.url})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    history = Detection.objects.filter(user=request.user)[:6]
    return render(request, "disease/disease.html", {"history": history})
