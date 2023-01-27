import json
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from jwt_auth.decorators import token_required
from monitoring.models import URL


# view to add a new url to monitor
# POST /api/monitoring/url/
@require_http_methods(["POST"])
@token_required
def add_url_view(request):
    urls_for_this_user = URL.objects.filter(owner=request.auth_user)
    if urls_for_this_user.count() >= 20:
        return JsonResponse({"message": "You can only monitor 20 urls"}, status=403)
    data = json.loads(request.body)
    url = data.get("url")
    if not url:
        return JsonResponse({"message": "URL is required"}, status=400)
    if not url.startswith("http"):
        url = "http://" + url
    error_threshold = data.get("error_threshold")
    if error_threshold:
        new_url = URL.objects.create(url=url, error_threshold=error_threshold,
                                     owner=request.auth_user)
    else:
        new_url = URL.objects.create(url=url, owner=request.auth_user)
    return JsonResponse({"message": "URL added successfully", "url": new_url.url},
                        status=201)


# view to get all urls for a user
# GET /api/monitoring/url/
@require_http_methods(["GET"])
@token_required
def get_urls_view(request):
    urls = URL.objects.filter(owner=request.auth_user)
    return JsonResponse({"urls": [url.url for url in urls]}, status=200)


# view to call url views
def urls_view(request):
    if request.method == "POST":
        return add_url_view(request)
    elif request.method == "GET":
        return get_urls_view(request)
    return JsonResponse({"message": "Method not allowed"}, status=405)


# view to see all heartbeat data for a url
# GET /api/monitoring/heartbeat/<url>/
@require_http_methods(["GET"])
@token_required
def get_heartbeat_view(request):
    url = request.GET.get("url")
    if not url:
        return JsonResponse({"message": "URL is required"}, status=400)
    if not url.startswith("http"):
        url = "http://" + url
    url = URL.objects.get(url=url)
    if not url:
        return JsonResponse({"message": "URL not found"}, status=404)
    if url.owner != request.auth_user:
        return JsonResponse({"message": "You are not authorized to view this url"},
                            status=401)
    past_24_hours = url.heartbeats.filter(
        created_at__gte=datetime.now() - timedelta(days=1))

    success_heartbeats = past_24_hours.filter(status__gte=200,status__lt=300)
    error_heartbeats = past_24_hours.filter(status__gte=400)
    is_alert = url.error_count >= url.error_threshold
    return JsonResponse(
        {
            "heartbeats": [heartbeat.to_dict() for heartbeat in past_24_hours],
            "success_heartbeats": success_heartbeats.count(),
            "error_heartbeats": error_heartbeats.count(),
            "is_alert": is_alert
         }, status=200)

# view to get all alerts
# GET /api/monitoring/alert/
@require_http_methods(["GET"])
@token_required
def get_alerts_view(request):
    urls = URL.objects.filter(owner=request.auth_user)
    alerts = []
    for url in urls:
        if url.error_count >= url.error_threshold:
            alerts.append(url.url)
    return JsonResponse({"alerts": alerts}, status=200)