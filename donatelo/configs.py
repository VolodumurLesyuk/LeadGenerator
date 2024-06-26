from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent   # /home/mykhailo/Programs/Web_Form_prog/LeadGenerator

conf_file = config("PATH_CONFIG_FILE")
config_file_path = BASE_DIR / conf_file

list_of_obj = [
    "UsrTypePartner",
    "UsrStatusPartnerESD",
    "UsrEmployeeStatus",
    "UsrLeadType",
    "UsrSourceLookup"
]
