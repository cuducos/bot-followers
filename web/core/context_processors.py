from django.conf import settings


def confidence(request):
    value = settings.Z_SCORE_CONFIDENCE_TABLE.get(settings.Z_SCORE)
    return {"CONFIDENCE": f"Errors for {value * 100:.0f}% confidence." if value else ""}
