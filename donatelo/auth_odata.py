import configparser
import requests
import urllib3
import json
from donatelo import configs
from decouple import config as decouple_config

config = configparser.ConfigParser()


def authenticate():
    config.read(configs.config_file_path)
    url = config['CREATIO']['auth_url']
    login = decouple_config("CRM_NAME")
    password = decouple_config("CRM_PASS")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    headers = {
        'Accept': 'application/json',
        'ForceUseSession': 'true',
        'Content-Type': 'application/json'
    }

    data = {
        'UserName': login,
        'UserPassword': password
    }

    response = requests.post(url=url, headers=headers, json=data, verify=False)

    if response.status_code == 200:
        base_path = configs.BASE_DIR
        path_response = base_path / config['CREATIO_AUTH_COOKIES']['path_response']
        path_cookies = base_path / config['CREATIO_AUTH_COOKIES']['path_cookies']

        with open(path_response, 'w') as response_file:
            json.dump(response.json(), response_file, indent=4, ensure_ascii=False)

        cookies = {cookie.name: cookie.value for cookie in response.cookies}

        with open(path_cookies, 'w') as cookies_file:
            json.dump(cookies, cookies_file, indent=4, ensure_ascii=False)
        print(f'Авторизація успішна')
        return True

    else:
        print(f'Помилка {response.status_code}: {response.text}')
        return False
