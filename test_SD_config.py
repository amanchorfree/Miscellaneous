import re
import json
import sys

with open(sys.argv[1], 'r') as full_file:
    config = full_file.read()
    print(config)

check_par = {"]":"[", "}":"{", ")":"("}

# Function to check parentheses
def check(config):
    stack = []
    for i in range(len(config)):
        if config[i] in check_par.values():
            stack.append(config[i])
        elif config[i] in check_par.keys():
            if len(stack) > 0:
                if stack.pop()!=check_par[config[i]]:
                    return False, i
            else:
                return False, i
    return True, 0

def return_key_value_recursively(d):
    l=[]
    for key, value in d.items():
        if type(value) == dict:
            l.extend(return_key_value_recursively(value))
        elif type(value) == list and type(value[0]) == dict:
            l.extend(return_key_value_recursively(value[0]))
        else:
            l.append([key,value])
    return l

def verify_json(my_config):
  try:
    json_object = json.loads(my_config)
    for config_values in return_key_value_recursively(json_object):
        if config_values[0]=='ips':
            for address in config_values[1]:
                if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', address) == None:
                    return False, address
  except ValueError:
    print("Check if all parenthis are closed: ", check(my_config))
    return False, check(my_config)
  return True

print(verify_json(config))

