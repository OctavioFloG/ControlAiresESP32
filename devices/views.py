from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
from .models import Device

# Create your views here.

def dashboard(request):
    devices = Device.objects.order_by("name")
    return render(request, "devices/dashboard.html", {"devices": devices})

@require_http_methods(["POST"])
def toggle_device(request, pk):
    device = get_object_or_404(Device, pk=pk)
    # Cambiamos el estado deseado; el ESP32 lo leerá y actuará
    device.desired_state = not device.desired_state
    device.save()
    messages.success(request, f"Comando enviado a {device.name}: {'ENCENDER' if device.desired_state else 'APAGAR'}")
    return redirect("devices:dashboard")

# --------- API (para ESP32) ----------
def _auth_device(api_key: str) -> Device | None:
    try:
        return Device.objects.get(api_key=api_key)
    except Device.DoesNotExist:
        return None

@csrf_exempt
@require_http_methods(["POST"])
def api_heartbeat(request):
    """
    ESP32 POSTea: api_key, is_on (0/1)
    Actualiza last_seen e is_on. Responde JSON ok.
    """
    api_key = request.POST.get("api_key")
    is_on = request.POST.get("is_on")
    if not api_key or is_on not in ("0","1"):
        return HttpResponseBadRequest("Missing or invalid params")

    device = _auth_device(api_key)
    if not device:
        return HttpResponseBadRequest("Invalid api_key")

    device.is_on = (is_on == "1")
    device.last_seen = timezone.now()
    device.save()
    return JsonResponse({"ok": True, "server_time": timezone.now().isoformat()})

@csrf_exempt
@require_http_methods(["GET"])
def api_command(request):
    """
    ESP32 GETea: api_key
    Retorna desired_state (0/1). El ESP32 actúa en consecuencia.
    """
    api_key = request.GET.get("api_key")
    if not api_key:
        return HttpResponseBadRequest("Missing api_key")

    device = _auth_device(api_key)
    if not device:
        return HttpResponseBadRequest("Invalid api_key")

    return JsonResponse({
        "desired_state": 1 if device.desired_state else 0,
        "device": device.name,
    })
