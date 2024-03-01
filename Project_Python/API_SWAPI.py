##HOMEWORK API name height weight gender homeworld

# import module
import requests as re
from time import sleep
import pandas as pd

url = "https://swapi.dev/api/people/"
# # get to url
# response = re.get(url)

# check status
# print(response.status_code)

result = []

for i in range(5):
  index = i+1
  new_url = url + str(index)
  resp = re.get(new_url).json()
  name = resp["name"]
  height = resp["height"]
  weight = resp["mass"]
  gender = resp["gender"]
  homeworld = re.get(resp["homeworld"]).json()["name"]
  #print(name, height, weight, gender, homeworld)
  sleep(1)
  result_api = {
    "name": name,
    "height": height,
    "weight": weight,
    "gender": gender,
    "homeworld": homeworld
  }
  result.append(result_api)

# Save as json
final_result = pd.DataFrame(result)
print(final_result)
final_result.to_json("swapi_homework.json")
