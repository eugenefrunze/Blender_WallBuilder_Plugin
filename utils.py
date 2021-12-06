import bpy
from bpy.utils import resource_path
import data_types
import urllib.request, json


#generate customers list from API
def get_customers_json():
    generated = []
    url = 'https://www.bauvorschau.com/plugins'
    responce = urllib.request.urlopen(url)
    customers = json.loads(responce.read())
    for idx, customer in enumerate(customers):
        generated.append((customer['ucm_id'], 'customer'+str(idx), ''))
    return generated