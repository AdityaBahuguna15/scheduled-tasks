import requests
from twilio.rest import Client
import os

API_KEY = os.environ.get("API_KEY_WEATHER")
MY_LAT = 41.902782
MY_LONG = 12.496365

account_sid = os.environ.get("ACC_SID")
auth_token = os.environ.get("AUTH_TOKEN")
client = Client(account_sid, auth_token)

paramaters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": API_KEY,
    "cnt": 4
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=paramaters)
response.raise_for_status()
data = response.json()

will_rain = False
for time in data["list"]:
    condition_code = time["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain=True
if will_rain:
    message = client.messages.create(
    from_=f'whatsapp:{os.environ.get("TWILIO_PHONE")}',
    body="It's going to rain, bring an umbrella!",
    to=f'whatsapp:{os.environ.get("MY_PHONE")}'
    )
    print(message.status)
else:
    print("No rain today.")
