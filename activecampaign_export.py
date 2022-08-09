import requests
import json
import csv
import pandas as pd
import find_path as fp
'''
AC docs: https://developers.activecampaign.com/reference/retrieve-fields?youraccountname=peaksiderealty
'''

API_KEY = '40ddd4d7744346d5064b3dd77bef3bc0635ce1b64059b85cf34c74b5435ece2d851573a2'
AC_BULK_IMPORT_URL = "https://peaksiderealty.api-us1.com/api/3/import/bulk_import"
AC_FIELDS_URL = "https://peaksiderealty.api-us1.com/api/3/fields"
AC_LISTS_URL = "https://peaksiderealty.api-us1.com/api/3/lists?limit=1000"

KEEP_LIST = ['Agent First Name:', 'Agent Last Name', 'Agent Email:', 'Agent Phone Number:', 'Agent Brokerage:',
            'Agent Website:', 'Brokerage Street Address', 'Agent City:', 'Inquiring on Property?', 
            'Property City', 'Property State', 'Property Zip Code', 'Phone 2', 'Lead Type']




#this loads the json file into a dict
#  with open('ac custom fields.json', 'r') as f:
#     ac_fields = json.load(f)

# pull field ids in a dict
# all_field_id_dict = fp.return_all_fields_ids(ac_fields)


# get the target ids from the dict
# target_ids = fp.return_target_field_ids(KEEP_LIST, ac_fields)
# for k,v in target_ids.items():
#     print(k,v)

def save_response_to_json(response, filename):
    '''
    save the json response to a file
    '''

    pretty_json = json.loads(response.text)
    with open(filename, "w") as write_file:
        json.dump(pretty_json, write_file, indent=4)

    return pretty_json


def get_all_lists(file_name, url=AC_LISTS_URL, key=API_KEY):
    '''
    get all lists from the api
    '''
    # url = "https://peaksiderealty.api-us1.com/api/3/lists?limit=1000"

    headers = {
        "Accept": "application/json",
        "Api-Token": key
    }

    response = requests.get(url, headers=headers)
    # lists = save_response_to_json(response, filename)
    return json.loads(response.text)


def create_contact_dict(contact, list_id):
    '''
    takes a dict and creates a dict for the AC api
    '''
    pass
    # contact_dict = {'tags': [], 'fields': [], 'subscribe': [], 'email': '', 'first_name': '', 'last_name': '', 'phone': ''} <-- this is the dict we want to create as template
    ac_dict = {}
    ac_dict['tags'] = [contact['FIRST'] + ' ' + contact['LAST'] + ' - ' + contact['Lead Type'], contact['Prop-Zip']]
    ac_dict['fields'] = [
                {
                    "id": 6,
                    "value": contact['Agent First Name']
                },
                {
                    "id": 16,
                    "value": contact['Agent Last Name']
                },
                {
                    "id": 10,
                    "value": contact['Agent Email']
                },
                {
                    "id": 9,
                    "value": contact['Agent Phone']
                },
                {
                    "id": 7,
                    "value": contact['Brokerage Name']
                },
                {
                    "id": 11,
                    "value": contact['Agent Website']
                },
                {
                    "id": 15,
                    "value": contact['Brokerage Address']
                },
                {
                    "id": 8,
                    "value": contact['Brokerage City']
                },
                {
                    "id": 1,
                    "value": contact['Prop_Address']
                },
                {
                    "id": 18,
                    "value": contact['Prop-City']
                },
                {
                    "id": 19,
                    "value": contact['Prop-State']
                },
                {
                    "id": 20,
                    "value": contact['Prop-Zip']
                },
                {
                    "id": 17,
                    "value": contact['Lead Type']
                },
           ]
    ac_dict['subscribe'] = [{'listid': list_id}]
    ac_dict['email'] = contact['EMAIL']
    ac_dict['first_name'] = contact['FIRST']
    ac_dict['last_name'] = contact['LAST']
    ac_dict['phone'] = contact['PHONE']

    return ac_dict


def reformat_contact_dict(contact_dict, list_id):
    '''takes list of dicts from to_dict and reformats them to a list of dicts for the AC api'''
    contacts = [] # [contact for contact in create_contact_dict(contact)] ?
    for contact in contact_dict:
        contacts.append(create_contact_dict(contact, list_id))
    return contacts
    

def update_lists_ac_api(contacts, range, url=AC_BULK_IMPORT_URL, key=API_KEY):
    '''
    needs work - auto suggested
    '''

    payload = {
        "contacts": contacts[:range],
        "callback": {
        "requestType": "POST",
        "detailed_results": "true",
        #current location for google cloud functions
        "url": "https://us-central1-quixotic-card-265402.cloudfunctions.net/receive_hook_process"
        }
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Api-Token": key
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

    # ac_dict['subscribe':] []
    #         "subscribe": [{"listid": "36"}, {"listid": "18"}]
    #         "email": "contact@email.com",
    #         "first_name": "first_name",
    #         "last_name": "last_name",
    #         "phone": "1111111111"


# all_lists = get_all_lists(AC_LISTS_URL, API_KEY, 'all lists updated.json')
# hiiq test list no = 41
#BEGIN TEMPLATE FOR UPLOAD (MINUS LIST ID)
# import requests

url = "https://peaksiderealty.api-us1.com/api/3/import/bulk_import"
def bulk_upload(url, key, contact_list):
    '''
    takes formatted list of contacts and uploads them to the AC api
    '''

    payload = {
        "contacts": contact_list,
        "callback": {
            "requestType": "POST",
            "detailed_results": "true",
            "url": "https://us-central1-quixotic-card-265402.cloudfunctions.net/receive_hook_process"
        }
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Api-Token": key,
              #current location for google cloud functions
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
#END TEMPLATE FOR UPLOAD

# import requests
# def get_ac_fields(key, url):
#     headers = {
#         "Accept": "application/json",
#         "Api-Token": key
#     }

#     response = requests.get(url, headers=headers)
#     return response

# def save_ac_fields(response):
#     pretty_json = json.loads(response.text)
#     with open("ac custom fields.json", "w") as write_file:
#         json.dump(pretty_json, write_file, indent=4)

#     return pretty_json


# here is the suggestion for bulk upload, custom fields updated via ID
# https://developers.activecampaign.com/reference/bulk-import-contacts

