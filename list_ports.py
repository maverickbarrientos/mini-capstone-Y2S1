import requests

url = "https://api.openweathermap.org/data/2.5/weather?lat=11.8397&lon=122.0714&appid=24d3d865b59dc30ac82dca45611bde4f"

response = requests.get(url)
print(response.status_code)
print(response.json())