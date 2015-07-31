import requests

def post(user, lat, lon, temp, light, zip, test = False):
  req = requests.get("http://data.sparkfun.com/input/aGOE6rY5mxcxX1GNnOKq?" +
  "private_key=KEo9nBl42xsZjRg94751" +
  "&user="        + ("test-" if test else "") + user +
  "&latitude=" 	  + str(lat) +
  "&longitude="   + str(lon) +
  "&temperature=" + str(temp) +
  "&light="       + str(light) +
  "&zip="         + str(zip)
  )

  return req.status_code
