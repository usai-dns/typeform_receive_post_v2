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
AC_GROUPS_URL = "https://peaksiderealty.api-us1.com/api/3/groups"
AC_LIST_GROUPS_URL = "https://peaksiderealty.api-us1.com/api/3/listGroups"

KEEP_LIST = ['Agent First Name:', 'Agent Last Name', 'Agent Email:', 'Agent Phone Number:', 'Agent Brokerage:',
            'Agent Website:', 'Brokerage Street Address', 'Agent City:', 'Inquiring on Property?', 
            'Property City', 'Property State', 'Property Zip Code', 'Phone 2', 'Lead Type']


# this loads the json file into a dict
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
    url = "https://peaksiderealty.api-us1.com/api/3/lists?limit=1000"

    headers = {
        "Accept": "application/json",
        "Api-Token": key
    }

    response = requests.get(url, headers=headers)
    # lists = save_response_to_json(response, filename)
    return json.loads(response.text)

def get_all_groups(file_name, url=AC_LISTS_URL, key=API_KEY):
    '''
    get all groups from the api
    '''

    headers = {
        "Accept": "application/json",
        "Api-Token": key
    }

    response = requests.get(url, headers=headers)
    groups = save_response_to_json(response, filename)
    return json.loads(response.text)

# def agent_list_check_builder(list_id_dict, agent_info_dict):
#     '''
#     build whichever lists are empty and return the ids, also needs lead type
#     '''
#     if not list_id_dict['Agent Target List Id']:
#         list_id_dict['Agent Target List Id'] = ac_create_agent_list(agent_info_dict)
#     if not list_id_dict['Agent Pending List Id']:
#         list_id_dict['Agent Pending List Id'] = ac_create_agent_list(agent_info_dict, pending=True)

#     return list_id_dict    


# def ac_create_agent_list(agent_info_dict, pending=False):
#     '''
#     create a list for the agent
#     '''
#     # url = "https://peaksiderealty.api-us1.com/api/3/lists"
#     url = "https://peaksiderealty.api-us1.com/api/3/lists"
#     headers = {
        
#         "Accept": "application/json",
#         "Api-Token": API_KEY
#     }
#     if pending:
#         name = agent_info_dict['Agent First Name'] + ' ' + agent_info_dict['Agent Last Name'] + ' - ' + agent_info_dict['Lead Type'] + ' - Pending'
#     else:
#         name = agent_info_dict['Agent First Name'] + ' ' + agent_info_dict['Agent Last Name'] + ' ' + agent_info_dict['Lead Type']

   ########################### create list in ac ################################


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
                    "value": contact['Brokerage Street Address'] #had inconsistent key
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

    
def create_agent_list(agent_info, list_type, url=AC_LISTS_URL, key=API_KEY):
    '''
    this needs to have the calls for agent info updated
    somewhere in here we need to return the new list id and add it to the governing list
    '''
    string_id = agent_info['Agent First Name'].lower() + '-' + agent_info['Agent Last Name'].lower() + '-' + agent_info['Lead Type'].lower().split()[0] + '-' + list_type.lower()
    payload = {"list": {
            "send_last_broadcast": False,
            "name": f"{agent_info['Agent First Name']} {agent_info['Agent Last Name']} - {agent_info['Lead Type']} - {list_type}",
            "stringid": string_id,
            "sender_url": f"{agent_info['Agent Website']}", #error here
            "sender_reminder": "click to unsubscribe",
            "user": 1,
            "fulladdress": ""
        }}

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Api-Token": key
    }

    response = requests.post(url, json=payload, headers=headers)
    print('ac create list api returns: ', response.text)
    return json.loads(response.text)['list']['id']



def agent_list_update(agent_info, list_id_dict, group_id = 3):
    '''
    create lists if they are empty
    this assigns the dict a list id, provided that create_agent_list returns the id successfully.
    '''
    if list_id_dict['target list id'] == None:
        list_id_dict['target list id'] = create_agent_list(agent_info, "Active")
        update_list_groups(list_id_dict['target list id'], group_id)
        print("active list created.")
    if list_id_dict['pending list id'] == None:
        list_id_dict['pending list id'] = create_agent_list(agent_info, "Pending")
        update_list_groups(list_id_dict['pending list id'], group_id)
        print("pending list created.")
    else:
        print('lists already exist')
        """
        only need to update groups if the permissions arent improved.
        """        
        # update_list_groups(list_id_dict['target list id'], group_id)
        # update_list_groups(list_id_dict['pending list id'], group_id)

    return list_id_dict


def update_list_groups(list_id, group_id=3, url=AC_LIST_GROUPS_URL, key=API_KEY):
    '''
    this miserable little shit updates a list to be visible to the admin
    '''

    payload = {"listGroup": {
          "listid": list_id,
          "groupid": group_id
      }}
    headers = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Api-Token": key
  }

    response = requests.post(url, json=payload, headers=headers)

    print('listGroup update from ac returns: ', response.text)



def update_lists_ac_api(contacts, url=AC_BULK_IMPORT_URL, key=API_KEY):
    '''
    this takes the transformed dict of contacts and bulk updates contacts
    contacts are updated to a list according to their list id attached to them in the contacts dict.
    '''

    payload = {
        "contacts": contacts,
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


def get_agent_contact_info(agent_email, key=API_KEY):
  #this function will search for a contact in AC via their email address and return the contact info
  url = 'https://peaksiderealty.api-us1.com/api/3/contacts?email=' + agent_email +'&status=-1&orders[email]=ASC'

  headers = {
    "Accept": "application/json",
    "Api-Token": key
  }

  response = requests.get(url, headers=headers)
  # pretty print in case we need to inspect the response
  pretty_json = json.loads(response.text)

  # create the structure of the agent info dict, with addition of contact ID
  agent_dict = {
  'Agent First Name': pretty_json['contacts'][0]['firstName'],
  'Agent Last Name': pretty_json['contacts'][0]['lastName'],
  'Agent Email': pretty_json['contacts'][0]['email'],
  'Agent Phone': pretty_json['contacts'][0]['phone'],
  'Agent Contact ID': pretty_json['contacts'][0]['id']
  }

  return agent_dict


def get_agent_fields(agent_id, agent_dict, key=API_KEY):
    # get all fields for agent back from AC
    # here are the static IDs for the fields we need

    field_number_values = {'7': 'Brokerage Name',
                       '8': 'Brokerage City',
                       '11': 'Agent Website',
                       '15': 'Brokerage Street Address',
                       }
    # create the url for the fields given the agent id
    url = "https://peaksiderealty.api-us1.com/api/3/contacts/" +agent_id + "/fieldValues"

    headers = {"Api-Token": key}

    response = requests.get(url, headers=headers)
    
    # just clean it up incase we need to inspect it
    pretty_json = json.loads(response.text)
    # iterate through the fields and return the values if the IDs match
    for field in pretty_json['fieldValues']:
      if field['field'] in field_number_values.keys():
        # this is the ugliest thing I've ever written.

        agent_dict[field_number_values[field['field']]] = field['value'] 
        
    return agent_dict


def get_agent_pipelines_deal_stages(agent_name):
  # get all pipelines and deal stages for an agent
  url = "https://peaksiderealty.api-us1.com/api/3/dealGroups?filters[title]=" + agent_name + "&orders[title]=ASC&orders[popular]=ASC"

  headers = {
      "Accept": "application/json",
      "Api-Token": "40ddd4d7744346d5064b3dd77bef3bc0635ce1b64059b85cf34c74b5435ece2d851573a2"
  }

  response = requests.get(url, headers=headers)
  return json.loads(response.text)




def get_stage_id(target_stage, agent_pipelines):
  # get id for a deal state
  for stage_name in agent_pipelines['dealStages']:
    if target_stage in stage_name['title'].lower():
      return stage_name['id']


#END TEMPLATE FOR UPLOAD

# import requests
# def get_ac_fields(key, url):
#     headers = {
#         "Accept": "application/json",
#         "Api-Token": key
#     }

#     response = requests.get(url, headers=headers)
#     return response

# def save_ac_fields(response, filename):
#     pretty_json = json.loads(response.text)
#     with open(filename, "w") as write_file:
#         json.dump(pretty_json, write_file, indent=4)

#     return pretty_json


# here is the suggestion for bulk upload, custom fields updated via ID
# https://developers.activecampaign.com/reference/bulk-import-contacts

