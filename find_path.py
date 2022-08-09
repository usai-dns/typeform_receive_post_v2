import json


# https://stackoverflow.com/questions/41777880/functions-that-help-to-understand-jsondict-structure/41778581#41778581 What a fucking hero


def find_key(obj, key):
    if isinstance(obj, dict):
        yield from iter_dict(obj, key, [])
    elif isinstance(obj, list):
        yield from iter_list(obj, key, [])


def iter_dict(d, key, indices):
    for k, v in d.items():
        if k == key:
            yield indices + [k], v
        if isinstance(v, dict):
            yield from iter_dict(v, key, indices + [k])
        elif isinstance(v, list):
            yield from iter_list(v, key, indices + [k])


def iter_list(seq, key, indices):
    for k, v in enumerate(seq):
        if isinstance(v, dict):
            yield from iter_dict(v, key, indices + [k])
        elif isinstance(v, list):
            yield from iter_list(v, key, indices + [k])


# def return_field_id(dct, key, target):
#     for item in dct[key]:
#         if target in item['title']:
#             return item['title'], item['id']


def return_field_id(dct, key, target):
    for item in dct[key]:
        if target == item['title']:
            return item['title'], item['id']


def return_all_fields_ids(dct):
    field_id_dict = {}
    for item in dct['fields']:
        field, id = item['title'], item['id']
        field_id_dict[field] = id
    return field_id_dict


def return_target_field_ids(keep_list, all_fields_dict):
    target_field_id_dict = {}
    for field_name in keep_list:
        target_field_id_dict[field_name] = return_field_id(all_fields_dict, 'fields', field_name)[1]
    return target_field_id_dict


def find_agent_list_id_json(agent_name, lead_type, lists_json):
  with open(lists_json) as f:
    lists = json.load(f)
  for list in lists['lists']:
    if agent_name in list['stringid'] and lead_type in list['stringid']:
      return list['id']


def find_agent_list_id_list(agent_name, lead_type, lists_list):
  for list in lists_list:
    if agent_name in list['stringid'] and lead_type in list['stringid']:
      return list['id']


# for field_name in keep_list:
#     if field_name in all_field_id_dict.keys():
#         print(field_name, 'found in field names')
#     else:
#         print(field_name, 'not found in field names')


# test_id = return_field_id(ac_fields, 'fields', keep_list[0])
# print(test_id)

# print(field_id_dict.keys())

# still needs work to make more univeral
# def return_field_id(dct, key, target):
#     for item in dct[key]:
#         if isinstance(item, dict):
#             for key in item.keys():
#                 if target in key:
#                     return key, item[key]
#         elif isinstance(item, list):
#             for element in item:
#                 for key in element.keys():
#                     if target in key:
#                         return key, element[key]

# BORKED
# def return_field_id_dict(lst, dct):
#     field_id_dict = {}
#     for item in lst:
#         field, id = return_field_id(dct, 'fields', item)
#         field_id_dict[field] = id
#     return field_id_dict


# keep_field_ids = return_field_id_dict(keep_list, ac_fields)
# for k,v in keep_field_ids.items():
#     print(k,v)

# print(field_id_dict.keys())

# field, id = return_id(ac_fields, 'fields', 'Agent First')
# field_ids = {field: id}