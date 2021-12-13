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
    
    print(generated)
    return generated


#geom nodes utils
def node_group_link(node_group, node1_output, node2_input):
    node_group.links.new(node1_output, node2_input)