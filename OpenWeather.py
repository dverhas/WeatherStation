import requests
from requests.auth import HTTPBasicAuth

owm_url = 'http://openweathermap.org/data/post'

def post(ctemp, pressure, humidity, altitude):
    payload = {'temp': ctemp, 'pressure':pressure, 'humidity':humidity, 'alt': altitude, 'name':'BackYard', 'lat':41.203404, 'long':-81.403038}
    r = requests.post(owm_url,data=payload, auth=HTTPBasicAuth('',''))
    print(r.text)

