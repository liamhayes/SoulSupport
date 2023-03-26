import requests
import json
API_KEY = '02712d4021416dafa258f93084d40dc7'

def local_weather(zip):
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?zip=" + zip + ",US&appid=02712d4021416dafa258f93084d40dc7&units=imperial"
    )
    j = response.json()
    # x = json.loads(json.dumps(j))
    # newVal = x['result']

    description = j['weather'][0]['description']
    feelsLike = j['main']['feels_like']
    print(description)
    print(feelsLike)  
    return [description, feelsLike]