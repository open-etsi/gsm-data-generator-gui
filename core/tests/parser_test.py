
import  json
from core.parser.utils import json_loader, ConfigHolder, ConfigData

JSON_PATH = "C:/Users/DELL/Desktop/datadecryption_poetry/core/settings.json"

if __name__ == "__main__":

    config_holder = json_loader(JSON_PATH)

    # Load config data
    with open(JSON_PATH, "r") as f:
        data = json.load(f)
    config = ConfigData(**data)
    config_holder = ConfigHolder.from_config(config)
    print(config_holder.DISP.imsi)
