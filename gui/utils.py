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


def is_valid_imsi(imsi: [int, "IMSI Length Validation"]) -> bool: # type: ignore
    return len(str(imsi)) == 15


def len_check(text, key_type, widget):
    var = int(parameter_len(text))
    if (var + 1) > len(key_type):
        widget.setStyleSheet(style_sheet_bad)
    else:
        widget.setStyleSheet(style_sheet_good)
