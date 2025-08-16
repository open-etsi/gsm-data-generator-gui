from typing import Annotated
from .stylesheet import style_sheet_disabled, style_sheet_good, style_sheet_bad


def parameter_len(param) -> str:
    """Function printing python version."""
    length = 0
    match param:
        case "ICCID_MIN":
            length = 18
        case "ICCID":
            length = 20
        case "IMSI":
            length = 15
        case "PIN1" | "PIN2" | "ACC":
            length = 4
        case "PUK1" | "PUK2" | "ADM1" | "ADM6":
            length = 8
        case "KI" | "EKI" | "OPC":
            length = 32
        case "K4":
            length = 64
        case "SIZE":
            length = 1
        case _:
            length = 32
    return str(length - 1)


def is_valid_iccid(iccid: Annotated[int, "ICCID length validation"]) -> bool:
    iccid_length = len(str(iccid))
    return iccid_length in [18, 19, 20]


def is_valid_imsi(imsi: [int, "IMSI Length Validation"]) -> bool:  # type: ignore
    return len(str(imsi)) == 15


def len_check(text, key_type, widget):
    var = int(parameter_len(text))
    if (var + 1) > len(key_type):
        widget.setStyleSheet(style_sheet_bad)
    else:
        widget.setStyleSheet(style_sheet_good)


def list_2_dict(list: list) -> dict:
    dict = {}
    for index in range(0, len(list)):
        dict[str(index)] = [list[index], "Normal", "0-31"]
    return dict


def dict_2_list(d: dict) -> list:
    list1 = []
    for index, j in enumerate(d):
        temp = list(d.values())[index][0]
        list1.append(temp)
    return list1


# # m_zong = ZongGenerateHandle()

# # m_zong.set_json_to_UI()
# # m_zong.Generate_laser_file("AAA",s.dataframes.GRAPH_DF)
# # m_zong.Generate_servr_file("ASD",s.dataframes.SERVR_DF)
# # m_zong.Generate_elect_file("ASD",s.dataframes.ELECT_DF)

import json


def read_json(file_path: str):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        return dict(data)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None  # You can choose to return None or raise a custom exception here
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in '{file_path}': {e}")
        return None  # You can choose to return None or raise a custom exception here


def copy_function(x):
    return str(x)
