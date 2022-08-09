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
AC_LISTS_URL = "https://peaksiderealty.api-us1.com/api/3/lists"

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




def save_JSON_fields(response, filename):
    '''
    save the json response to a file
    '''

    pretty_json = json.loads(response.text)
    with open(filename, "w") as write_file:
        json.dump(pretty_json, write_file, indent=4)

    return pretty_json


def get_all_lists(url, key, filename):
    '''
    get all lists from the api
    '''
    url = "https://peaksiderealty.api-us1.com/api/3/lists"

    headers = {
        "Accept": "application/json",
        "Api-Token": key
    }

    response = requests.get(url, headers=headers)
    lists = save_JSON_fields(response, filename)
    return response

#BEGIN TEMPLATE FOR UPLOAD (MINUS LIST ID)
# import requests

# url = "https://peaksiderealty.api-us1.com/api/3/import/bulk_import"

# payload = {
#     "contacts": [
#         {
#             "tags": ["zipcode_tag, list_type_tag"],
#             "fields": [
#                 {
#                     "id": 6,
#                     "value": "agent_first_name"
#                 },
#                 {
#                     "id": 16,
#                     "value": "agent_last_name"
#                 },
#                 {
#                     "id": 10,
#                     "value": "agent_email"
#                 },
#                 {
#                     "id": 9,
#                     "value": "agent_phone"
#                 },
#                 {
#                     "id": 7,
#                     "value": "agent_brokerage"
#                 },
#                 {
#                     "id": 11,
#                     "value": "aegnt_website"
#                 },
#                 {
#                     "id": 15,
#                     "value": "brokerage_street_address"
#                 },
#                 {
#                     "id": 8,
#                     "value": "agent_city"
#                 },
#                 {
#                     "id": 1,
#                     "value": "inquiring_on_property"
#                 },
#                 {
#                     "id": 18,
#                     "value": "property_city"
#                 },
#                 {
#                     "id": 19,
#                     "value": "property_state"
#                 },
#                 {
#                     "id": 20,
#                     "value": "property_zip"
#                 },
#                 {
#                     "id": 17,
#                     "value": "lead_type"
#                 }
#             ],
#             "email": "contact@email.com",
#             "first_name": "first_name",
#             "last_name": "last_name",
#             "phone": "1111111111"
#         }
#     ],
#     "callback": {
#         "requestType": "POST",
#         "detailed_results": "true"
#     }
# }
# headers = {
#     "Accept": "application/json",
#     "Content-Type": "application/json",
#     "Api-Token": "40ddd4d7744346d5064b3dd77bef3bc0635ce1b64059b85cf34c74b5435ece2d851573a2"
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.text)
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

'''
need to create a function which pairs titles and ids so i can match strings to
keys, and use the keys to find the ids.
if key contains zip, return dict[key] (for the id)

then we need to generate fucking HUGE json file from the csv,
or do it right from the original dataframe
'''
# import requests

# url = "https://peaksiderealty.api-us1.com/api/3/import/bulk_import"

# payload = {"callback": {
#         "requestType": "POST",
#         "detailed_results": "true"
#     }}
# headers = {
#     "Accept": "application/json",
#     "Content-Type": "application/json",
#     "Api-Token": "40ddd4d7744346d5064b3dd77bef3bc0635ce1b64059b85cf34c74b5435ece2d851573a2"
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.text)