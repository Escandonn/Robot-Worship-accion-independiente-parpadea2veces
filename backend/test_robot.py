import requests
import json

url = "http://127.0.0.1:8000/api/v1/robot/interpret"
data = {"text": "Hola Risp, ¿cómo estás?"}

response = requests.post(url, json=data)
print("Status:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2, ensure_ascii=False))
