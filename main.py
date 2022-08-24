from flask import Flask, request, render_template
import json
import pandas as pd
import find_path as fp
import clean_data as cld
import intake_data as id
import activecampaign_export as ace
'''
next step is to get the dataframe into a format where we can create the upload json file
for activecampaign

template upload is commented out in activecampaign_export.py
format (aside from list ids), is correct for the custom fields

incoming data column names need to be matched to the field names in AC

convert df to list of dicts - then create a new dict with the values in the correct format for ac upload.
https://pynative.com/convert-pandas-dataframe-to-dict/#:~:text=When%20we%20have%20a%20DataFrame%20with%20row%20indexes%20and%20if,is%20created%20for%20each%20row.
'''


data = id.create_test_dict('typeform test data.json')
transformed_data = id.typeform_response_dict(data)
# create a dict with the agent info from typeform
this_agent_dict = cld.agent_info_dict(transformed_data)

# get the list of lists from the activecampaign api - currently skipped as we're pulling from the api
lists = ace.get_all_lists('all lists updated.json')

with open('pulled list data.json', 'w', encoding='utf-8') as f:
    json.dump(lists, f, ensure_ascii=False, indent=4)
## lists exist, but i think the Links section needs to be amended for them to be visible in the AC UI
# get the list id for the agent by type of lead
list_id_dict = fp.return_agent_list_id(this_agent_dict['Agent First Name'], this_agent_dict['Lead Type'], lists)
for k,v in list_id_dict.items():
    print('found', k, ': ', v)


# check if the list id is found, if not create it and return list id
updated_list_ids = ace.agent_list_update(this_agent_dict, list_id_dict)
for k,v in updated_list_ids.items():
    print('updated: ', k, ': ', v)
# # transform dataframe and add agent info to entries
# # calls intake data to get the dataframe from csv
# # calls add_agent_info to add agent info to dataframe
clean_df = cld.combined_clean(this_agent_dict)
# print(clean_df.head())

# # convert the dataframe to a list of dicts with pandas 'records' format
contact_list_from_df = clean_df.to_dict('records')

# '''reformat the dicts to match the activecampaign api
# this needs to get adjusted to that it only pulls the UPDATE_CHUNK_SIZE number of dicts at a time
# then we can put the remaining dicts in the pending list and update the api
# '''
contact_list = ace.reformat_contact_dict(contact_list_from_df[:UPDATE_CHUNK_SIZE], updated_list_ids['target_list_id'])
pending_contact_list = ace.reformat_contact_dict(contact_list_from_df[UPDATE_CHUNK_SIZE:], updated_list_ids['pending_list_id'])
# # print(contact_list[:1]) # test to see if the dict is formatted correctly

# # upload the list of dicts to the activecampaign api
ace.update_lists_ac_api(contact_list)
ace.update_lists_ac_api(pending_contact_list)


# ################################################
# UPDATE_CHUNK_SIZE = 300

# app = Flask("app",
#   template_folder="templates", # name of folder containing html templates
#   static_folder="static" # name of folder for static files
# )

# @app.route("/", methods=['GET', 'POST'])
# def submit():
#   if request.method == 'POST':
#     # get the json file from the form
#     data = request.json
#     # transform the json file into a dict
#     transformed_data = id.typeform_response_dict(data)
#     # create a dict with the agent info from typeform
#     this_agent_dict = cld.agent_info_dict(transformed_data)
#     # get the list of lists from the activecampaign api
#     lists = ace.get_all_lists('all lists updated.json')
#     # get the list id for the agent by type of lead
#     list_id_dict = fp.return_agent_list_id(this_agent_dict['Agent First Name'], this_agent_dict['Lead Type'], lists)
#     # check if the list id is found, if not create it and return list id
#     updated_list_ids = agent_list_update(this_agent_dict, list_id_dict)
  

#     # transform dataframe and add agent info to entries
#     # calls intake data to get the dataframe from csv
#     # calls add_agent_info to add agent info to dataframe
#     clean_df = cld.combined_clean(this_agent_dict)
#     print(clean_df.head())

#     # convert the dataframe to a list of dicts
#     contact_list_from_df = clean_df.to_dict('records')

#     '''reformat the dicts to match the activecampaign api
#     this needs to get adjusted to that it only pulls the UPDATE_CHUNK_SIZE number of dicts at a time
#     then we can put the remaining dicts in the pending list and update the api
#     '''
#     contact_list = ace.reformat_contact_dict(contact_list_from_df[:UPDATE_CHUNK_SIZE], updated_list_ids['target_list_id'])
#     pending_contact_list = ace.reformat_contact_dict(contact_list_from_df[UPDATE_CHUNK_SIZE:], updated_list_ids['pending_list_id'])
#     # print(contact_list[:1]) # test to see if the dict is formatted correctly

#     # upload the list of dicts to the activecampaign api
#     ace.update_lists_ac_api(contact_list)
#     ace.update_lists_ac_api(pending_contact_list)


#     -return "webhook received"


    
#   else:
#     return "nothing"
  
# app.run(host="0.0.0.0", port=8080) # run the application
# ##############################################

