import bpy
from . import data_types
import urllib.request, json

#generate customers list from API
def get_customers_info():
    generated = []
    url = 'https://www.bauvorschau.com/api/clients_measures'
    responce = urllib.request.urlopen(url)
    customers = json.loads(responce.read())
    data_types.customers_json = customers
    for customer in customers:
        generated.append((customer['ucm_id'], customer['mc_name'], ''))
    return generated


def get_customers_json_new():
    generated =[]


#geom nodes utils
def node_group_link(node_group, node1_output, node2_input):
    node_group.links.new(node1_output, node2_input)