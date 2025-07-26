from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
import random
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Store latest location data in memory
latest_route = {}
from django.http import JsonResponse
import requests

@api_view(['GET'])
def directions_proxy(request):
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    key = 'AIzaSyCzPpjsrF--MkMLHaFLsHkxRPQxZohV10s'  # Replace with your actual API key

    if not origin or not destination:
        return JsonResponse({'error': 'origin and destination required'}, status=400)

    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={key}'
    response = requests.get(url)
    return JsonResponse(response.json())

@api_view(['POST'])
def set_route(request):
    start = request.data.get("start")
    end = request.data.get("end")

    if not start or not end:
        return Response({"error": "Both start and end are required"}, status=400)

    # Save in memory
    latest_route["start"] = start
    latest_route["end"] = end

    return Response({"message": "Route saved successfully", "start": start, "end": end})


@api_view(['GET'])
def get_route(request):
    if "start" not in latest_route or "end" not in latest_route:
        return Response({"error": "No route set yet"}, status=404)

    return Response({
        "start": latest_route["start"],
        "end": latest_route["end"]
    })

@api_view(['GET'])
def junction_status(request):
    junction_names = ["Kottakkal", "Tirur", "Valanchery"]
    data = []

    for name in junction_names:
        count = random.randint(5, 60)  # Simulated vehicle count
        if count > 40:
            signal = "GREEN"
            alert = "🚨 Heavy congestion detected"
        elif count > 20:
            signal = "YELLOW"
            alert = "⚠️ Moderate traffic"
        else:
            signal = "RED"
            alert = "✅ Low traffic"

        data.append({
            "name": name,
            "vehicle_count": count,
            "signal": signal,
            "alert": alert
        })

    return Response({
        "timestamp": datetime.datetime.now().isoformat(),
        "junctions": data
    })
