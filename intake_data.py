import json
import clean_data as cld
import pandas as pd
import activecampaign_export as ace
import find_path as fp
import requests

def create_test_dict(json_file):
    '''
    this just pulls the typeform json instead of the request
    '''
    with open(json_file) as json_file:
        data = json.load(json_file)
    return data


def typeform_response_dict(data):
    '''
    create a dict from the typeform data
    '''
    questions = []
    answers = []
    for entry in data['form_response']['definition']['fields']:
      questions.append(entry['title'])
  
    for entry in data['form_response']['answers']:
      item_type = entry['type']
      if item_type == 'choice':
        answers.append(entry['choice']['label'])
      else:
        answers.append(entry[item_type])

    answer_dict = {}
    
    for pair in zip(questions, answers):
      answer_dict[pair[0]] = pair[1]
    
    return answer_dict

# data = create_test_dict('typeform test data.json')

# type_form_data = typeform_response_dict(data)
# this_agent_dict = cld.agent_info_dict(type_form_data)

# work_df = cld.intake_data(this_agent_dict)
# print(work_df.head())

# clean_df = cld.combined_clean(this_agent_dict)
# print(clean_df.head())
# contact_dict = clean_df.to_dict('records')
# print(contact_dict[0:1])
# for k,v in type_form_data.items():
#     print(k, ': ', v)

# print(this_agent_dict.values())

# work_df = cld.intake_data(working_dict)
# clean_df = cld.combined_clean(work_df)

# print('done')