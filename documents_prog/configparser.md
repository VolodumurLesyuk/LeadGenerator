# У цьому файлі описується базові операції із configparser


Ось приклад коду у потрібному файлі:
---

```from donatelo.configs import config_file_path``` - це файл з таким кодом:
        from pathlib import Path
        from decouple import config
        
        BASE_DIR = Path(__file__).resolve().parent.parent   # /home/mykhailo/Programs/Web_Form_prog/LeadGenerator
        
        conf_file = config("PATH_CONFIG_FILE")
        config_file_path = BASE_DIR / conf_file
---     
Тут виконується самий звичайний імпорт потрібних нам ліб
---
        import configparser
        from donatelo.configs import config_file_path
        config = configparser.ConfigParser()
        
---
Це приклад як можна записати з нуля конфігурації у файл 
---

        def test_write_to_config(config_file=config_file_path):
            config['DEFAULT'] = {
                'ServerAliveInterval': '45',
                'Compression': 'yes',
                'CompressionLevel': '9',
                'ForwardX11': 'yes'
            }
        
            config['bitbucket.org'] = {
                'User': 'hg'
            }
        
            config['topsecret.server.com'] = {
                'Host Port': '50022',
                'ForwardX11': 'no'
            }
        
            # Зберігаємо конфігураційний файл
            with open(config_file, 'w') as configfile:
                config.write(configfile)
        
---
У цьому прикладі показано операцію зміни у існуючій конфігурації потрібних нам параметрів
---
        def test_write_existing_config(config_file=config_file_path):
            config.read(config_file)
        
            config['DEFAULT']['ForwardX11'] = 'no'
            config['topsecret.server.com']['Host Port'] = '50023'
        
            config['newsection'] = {
                'NewKey1': 'NewValue1',
                'NewKey2': 'NewValue2'
            }
        
            with open(config_file, mode='w') as configfile:
                config.write(configfile)
        
---     
Тут показано видалення з файлу непотрібних нам параметрів і цілих блоків
---

        def test_remove(config_file=config_file_path):
            config.read(config_file)
        
            # Видалення налаштувань
            config.remove_option('topsecret.server.com', 'ForwardX11')
        
            # Видалення секції
            config.remove_section('newsection')
        
            with open(config_file, mode='w') as configfile:
                config.write(configfile)
        
        
