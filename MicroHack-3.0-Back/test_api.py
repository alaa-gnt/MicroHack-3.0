
import requests
import json

API_URL = "http://localhost:8000/api/v1/analytics/dashboard"

try:
    print(f"Testing API: {API_URL}")
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        data = response.json()
        print("API Response Success!")
        metrics = data.get("metrics", {})
        print("Metrics received:")
        print(json.dumps(metrics, indent=2))
        
        alerts_today = metrics.get("alerts_today")
        print(f"alerts_today in response: {alerts_today}")
    else:
        print(f"API Failed: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"Error: {e}")
