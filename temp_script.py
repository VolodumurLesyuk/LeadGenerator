# ------------ usable code--------------------

# from donatelo.constructor import send_lead_test, create_file_json_of_obj_dictionaries
# from donatelo.auth_odata import authenticate
#
# dat = authenticate()
# print(dat)
# # send_lead_test()
# create_file_json_of_obj_dictionaries()

# ----------------------
# ________Checker ___________

# import configparser
# from donatelo import configs
# config = configparser.ConfigParser()
#
#
# config.read(configs.config_file_path)
#
# data = config['PARTNER']
# for elem in data:
#     # print(elem, data[elem])
#     print(data[elem].split('/'))
# print(data)


#   _____________

from donatelo.constructor import select_allowed_uuid_by_name_param, req_crm_partner_take_all
from donatelo.auth_odata import authenticate
dat = authenticate()
#
# select_allowed_uuid_by_name_param()
req_crm_partner_take_all()