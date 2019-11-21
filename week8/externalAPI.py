import json
import requests
from flask import Flask, request

app = Flask(__name__)

api_token = 'INSERT_API_KEY_HERE'
api_url_base = 'https://developers.zomato.com/api/v2.1/'

headers = {'Content-Type': 'application/json',
           'user-key': api_token}

def get_city_entity(query):
    api_url = '{}locations?query={}'.format(api_url_base, query)
    print(api_url)
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        entity_id = data['location_suggestions'][0]['entity_id']
        return entity_id
    else:
        return None

def get_restaurants(city_name):
    entity_id = get_city_entity(city_name)
    api_url = '{}search?entity_id={}'.format(api_url_base, entity_id)
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['restaurants']
    else:
        return None

@app.route("/<location>", methods=['GET'])
def search_location(location):
    restaurants = get_restaurants(location)
    res_list = list()
    for res in restaurants:
        res_list.append(res['restaurant']['name'])
    return ', '.join(res_list)
