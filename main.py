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
this_agent_dict = cld.agent_info_dict(transformed_data)
clean_df = cld.combined_clean(this_agent_dict)
print(clean_df.head())
contact_list_from_df = clean_df.to_dict('records')
contact_list = ace.reformat_contact_dict(contact_list_from_df)
print(contact_list[:1])
ace.update_lists_ac_api(contact_list, 5)

######
# app = Flask("app",
#   template_folder="templates", # name of folder containing html templates
#   static_folder="static" # name of folder for static files
# )

# @app.route("/", methods=['GET', 'POST'])
# def submit():
#   if request.method == 'POST':
    ## get the json file from the form
    # data = request.json
    # transformed_data = id.typeform_response_dict(data)
    # this_agent_dict = cld.agent_info_dict(transformed_data)
    # clean_df = cld.combined_clean(this_agent_dict)
    # contact_list_from_df = clean_df.to_dict('records')
    # contact_list = ace.reformat_contact_dict(contact_list_from_df)
    #then update list in ac, function pending. update_list_ac_api(contact_list)


#     return "webhook received"


    
#   else:
#     return "nothing"
  
# app.run(host="0.0.0.0", port=8080) # run the application
######


#everything below was moved to another module

    # questions = []
    # answers = []
    # for entry in data['form_response']['definition']['fields']:
    #   questions.append(entry['title'])
  
    # for entry in data['form_response']['answers']:
    #   item_type = entry['type']
    #   if item_type == 'choice':
    #     answers.append(entry['choice']['label'])
    #   else:
    #     answers.append(entry[item_type])

    # answer_dict = {}
    
    # for pair in zip(questions, answers):
    #   answer_dict[pair[0]] = pair[1]

    # this_agent_dict = cld.agent_info_dict(answer_dict)
 
    # print(this_agent_dict['List Path'])
    # work_df = pd.read_csv(this_agent_dict['List Path'])
      
          
    # work_df = cld.combined_clean(this_agent_dict)

    # cld.output_csvs(work_df, this_agent_dict, 300)

    
    # for key in this_agent_dict.keys():
    #   print(key, ': ', this_agent_dict[key])

    # for pth in fp.find_key(data, 'title'):
    #   print(pth)




  # if request.method == 'GET':
  #   pass
    # text = request.args['TEXT']
    # return text
  # elif request.method == 'POST':
  #   data = request.json
  #   print("Data received from webhook is: ", request.json)
  #   return "webhook received!"


# def index():
  # return render_template("index.html")
  # return "hello world"

# @app.route("/submit", methods=['GET', 'POST'])
# def submit():
#   if request.method == 'GET':
#     text = request.args['TEXT']
#     return text
#   elif request.method == 'POST':
#     data = request.json
#     print("Data received from webhook is: ", request.json)
#     return "webhook received!"

