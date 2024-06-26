from decouple import config as decouple_config
from donatelo import configs

import json
import requests
import configparser


config = configparser.ConfigParser()


def ready_cookies():
    config.read(configs.config_file_path)
    base_path = configs.BASE_DIR
    cookies_filename = path_cookies = base_path / config['CREATIO_AUTH_COOKIES']['path_cookies']
    with open(cookies_filename, 'r') as cookies_file:
        cookies = json.load(cookies_file)

    return cookies


def write_to_temp_jsons(name_file, data):
    config.read(configs.config_file_path)
    base_path = configs.BASE_DIR
    created_file = base_path / config['FILE_JSON']['path_to_dir'] / (name_file + '.json')

    with open(created_file, 'w') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def send_lead_test():
    config.read(configs.config_file_path)
    url = config['CREATIO']['leads_url']

    base_path = configs.BASE_DIR

    cookies_filename = path_cookies = base_path / config['CREATIO_AUTH_COOKIES']['path_cookies']

    with open(cookies_filename, 'r') as cookies_file:
        cookies = json.load(cookies_file)

    headers = {
        'Accept': 'application/json',
        'ForceUseSession': 'true'
    }

    for item in cookies:
        headers[item] = cookies[item]

    data = {
        'UsrLeadName': 'Tester',
        'UsrLeadSurname': 'Serg',
        'UsrLeadPhoneNumber': '+380655656545'
    }

    response = requests.post(url, headers=headers, json=data, verify=False, cookies=cookies)

    print(f'response.text: {response.text}\nresponse.status_code: {response.status_code}')


def get_data_obj_crm(obj_name: str, cookies_path):
    config.read(configs.config_file_path)
    url = config['CREATIO']['default_url_odata'] + "/" + obj_name
    with open(cookies_path, 'r') as cookies_file:
        cookies = json.load(cookies_file)

    response = requests.get(url, cookies=cookies, verify=False)
    list_param_obj = [config[f'{obj_name}'][elem] for elem in config[f'{obj_name}']]
    data = response.json()["value"]
    print(data)
    res_data = dict()
    count = 0
    for item in data:
        res_data[count] = {param: item[param] for param in list_param_obj}
        count += 1
    return res_data


def create_file_json_of_obj_dictionaries(list_of_dicts=configs.list_of_obj):
    config.read(configs.config_file_path)
    cookies_path = configs.BASE_DIR / config['CREATIO_AUTH_COOKIES']['path_cookies']
    for obj in list_of_dicts:
        path_to_json = configs.BASE_DIR / config['FILE_JSON']['path_to_dir'] / (obj + ".json")

        res_data = get_data_obj_crm(obj, cookies_path)
        with open(path_to_json, 'w') as json_file:
            json.dump(res_data, json_file, indent=4, ensure_ascii=False)

        print(f'{obj} json created')


def select_allowed_uuid_by_name_param():
    config.read(configs.config_file_path)
    data_configs = config['PARTNER']
    res_dict = dict()
    count = 0
    for elem in data_configs:
        dict_str = data_configs[elem]
        res_dict[count] = json.loads(dict_str)
        count += 1
    # return res_dict

    data_allow_param = config['PARTNER']['dict_allowed_param']
    data_param_section = config['PARTNER']['dict_param_to_section']
    data_allow_param = json.loads(data_allow_param)
    data_param_section = json.loads(data_param_section)

    dict_selected_param_uuid = dict()

    for key, value in data_allow_param.items():
        if key not in data_param_section.keys():
            print(f'{key} not in data_allow_param')
        else:
            list_allowed_param = value.split("/")
            path_to_json_file = configs.BASE_DIR / config['FILE_JSON']['path_to_dir'] / (
                        data_param_section[key] + ".json")

            with open(path_to_json_file, 'r') as json_file:
                data_file = json.load(json_file)

            for item in data_file:
                name_par = data_file[item]["Name"]
                uuid_par = data_file[item]["Id"]
                if data_file[item]["Name"] in list_allowed_param:
                    print(uuid_par, ":", name_par, ":", data_param_section[key], ":", key)
                    dict_selected_param_uuid[uuid_par] = key

    inverted_dict = {}

    # Ітеруємося по оригінальному словнику
    for key, value in dict_selected_param_uuid.items():
        if value not in inverted_dict:
            inverted_dict[value] = []
        inverted_dict[value].append(key)

    # print(inverted_dict) -->
    #   {
    # 'UsrPartnerTypeId': ['ad63bf94-f0d1-4a63-9b24-87a6e0f990de',
    #                       'e10c49a7-540e-479d-b662-e955db9042be',
    #                       '2f5d548c-533f-4ffb-b8a2-2c38451eee5d'],
    # 'UsrLookupStatusPartnerESDId': ['338d10e1-ebb3-4d99-92bd-747f370e30b4',
    #                                 '23d8e863-fdb3-46d3-9012-c668d40ddab4']
    #   }

    return inverted_dict


def matches_filter(sub_dict, filter_dict):
    for key, values in filter_dict.items():
        if key in sub_dict and sub_dict[key] not in values:
            return False
    return True


def req_crm_partner_take_all():
    config.read(configs.config_file_path)
    empty_url = config['CREATIO']['default_url_odata']
    list_par = [config['Account'][par] for par in config['Account']]
    filter_str = ','.join(list_par)
    full_url = empty_url + "/Account/?$select=" + filter_str

    response = requests.get(full_url, verify=False, cookies=ready_cookies())
    try:
        data = response.json()["value"]
    except Exception as e:
        print("Error; ", e)
        return None

    allowed_data = select_allowed_uuid_by_name_param()

    filtered_dict = [v for v in data if matches_filter(sub_dict=v,
                                                       filter_dict=allowed_data)]

    print(len(filtered_dict))
    write_to_temp_jsons("Account", filtered_dict)
