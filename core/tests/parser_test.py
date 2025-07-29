import json
from core.parser.utils import json_loader, ConfigHolder, ConfigData, gui_loader


JSON_PATH = "D:/STC_APP/improvements/security-layer/datadecryption_poetry/settings.json"

json_var = {
    "DISP": {
        "elect_data_sep": ".",
        "server_data_sep": ".",
        "graph_data_sep": ".",
        "K4": "1111111111111111111111111111111111111111111111111111111111111111",
        "op": "11111111111111111111111111111111",
        "imsi": "111111111111111",
        "iccid": "1111111111111111111",
        "pin1": "1111",
        "puk1": "11111111",
        "pin2": "1111",
        "puk2": "11111111",
        "adm1": "11111111",
        "adm6": "11111111",
        "acc": "1111",
        "size": 25,
        "prod_check": True,
        "elect_check": True,
        "graph_check": True,
        "server_check": True,
        "pin1_fix": False,
        "puk1_fix": False,
        "pin2_fix": False,
        "puk2_fix": False,
        "adm1_fix": False,
        "adm6_fix": False,
    },
    "PATHS": {
        "TEMPLATE_JSON": "operators/zong/template.json",
        "INPUT_FILE_PATH": "",
        "INPUT_CSV": "operators/zong/input_dataframe.csv",
        "OUTPUT_FILES_DIR": "output_files1",
        "OUTPUT_FILES_LASER_EXT": "laser_extracted",
    },
    "PARAMETERS": {
        "server_variables": [
            "IMSI",
            "EKI",
            "ICCID",
            "PIN1",
            "PUK1",
            "PIN2",
            "PUK2",
            "ADM1",
            "ADM6",
        ],
        "data_variables": [
            "IMSI",
            "ICCID",
            "PIN1",
            "PUK1",
            "PIN2",
            "PUK2",
            "ADM1",
            "ADM6",
            "KI",
            "OPC",
            "ACC",
            "KIC1",
            "KID1",
            "KIK1",
            "KIC2",
            "KID2",
            "KIK2",
            "KIC3",
            "KID3",
            "KIK3",
        ],
        "laser_variables": {
            "0": ["ICCID", "Normal", "0-20"],
            "1": ["ICCID", "Normal", "0-20"],
            "2": ["ICCID", "Normal", "0-3"],
            "3": ["ICCID", "Normal", "4-7"],
            "4": ["ICCID", "Normal", "8-11"],
            "5": ["ICCID", "Normal", "12-15"],
            "6": ["ICCID", "Normal", "16-20"],
            "7": ["PIN1", "Normal", "0-3"],
            "8": ["PUK1", "Normal", "0-7"],
            "9": ["PIN2", "Normal", "0-3"],
            "10": ["PUK2", "Normal", "0-7"],
        },
    },
}


if __name__ == "__main__":
    # TEST GUI LOADER
    config_holder = gui_loader(json_var)
    print(config_holder.DISP.graph_data_sep)

    # TEST JSON FILE LOADER
    #    Load config data
    config_holder = json_loader(JSON_PATH)
    print(config_holder.DISP.pin1_fix)
