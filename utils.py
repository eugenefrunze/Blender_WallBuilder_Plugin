import bpy
from . import data_types
import urllib.request, urllib.error, json
from json.decoder import JSONDecodeError

#generate customers list from API
def get_customers_info():
    interface_list_generated = []
    url = 'https://www.bauvorschau.com/api/clients_measures2'
    errmessage = 'BBP->Utils->get_customers_info(): '
    try:
        responce = urllib.request.urlopen(url)
    except urllib.error.URLError as err:
        print(errmessage, err)
        return [('NO_CUST', 'NO CUSTOMERS DATA HAS GOTTEN', 'error in the BBP->Utils->get_customers_info()->urlopen()')]
    else:
        try:
            customers = json.loads(responce.read())
        except JSONDecodeError as err:
            print(errmessage, err)
            return [('NO_CUST', 'NO CUSTOMERS DATA HAS GOTTEN', 'error in the BBP->Utils->get_customers_info()->json.loads()')]
        else:
            data_types.customers_json = customers
            for customer in customers:
                interface_list_generated.append((customer['ucm_id'], customer['mc_name'], ''))
            return interface_list_generated
            

#geom nodes utils
def node_group_link(node_group, node1_output, node2_input):
    node_group.links.new(node1_output, node2_input)