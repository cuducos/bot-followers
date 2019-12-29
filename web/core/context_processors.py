from django.conf import settings


def confidence(request):
    value = settings.Z_SCORE_CONFIDENCE_TABLE.get(settings.Z_SCORE)
    return {"CONFIDENCE": f"Errors for {value} confidence." if value else ""}
