from flask import Flask, request, render_template
import json
import pandas
import find_path as fp
import clean_data as cld

app = Flask("app",
  template_folder="templates", # name of folder containing html templates
  static_folder="static" # name of folder for static files
)

@app.route("/", methods=['GET', 'POST'])
def submit():
  if request.method == 'POST':
    # json_dump = json.dumps
    data = request.json
    # assume you have the following dictionary
    # with open("test data.json", "w") as write_file:
    #   json.dump(data, write_file, indent=4)
    # print("Data received from webhook is: ", type(data))
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

    this_agent_dict = cld.agent_info_dict(answer_dict)

    work_df = cld.combined_clean(this_agent_dict)

    cld.output_csvs(work_df, this_agent_dict, 300)
    # for key in this_agent_dict.keys():
    #   print(key, ': ', this_agent_dict[key])

    # for pth in fp.find_key(data, 'title'):
    #   print(pth)

    
    
    return "webhook received!" 

    
  else:
    return "nothing"
  
app.run(host="0.0.0.0", port=8080) # run the application


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

app.run(host="0.0.0.0", port=8080) # run the application