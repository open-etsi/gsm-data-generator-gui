from pydantic import BaseModel, Field, conint, constr
from dataclasses import dataclass
from typing import List, Dict
import json


class DISP(BaseModel):
    elect_data_sep: str = Field(..., min_length=1)
    server_data_sep: str = Field(..., min_length=1)
    graph_data_sep: str = Field(..., min_length=1)
    K4: constr(min_length=64, max_length=64)  # type: ignore
    op: constr(min_length=32, max_length=32)  # type: ignore
    imsi: constr(min_length=15, max_length=15)  # type: ignore
    iccid: constr(min_length=18, max_length=19)  # type: ignore
    pin1: constr(min_length=4, max_length=4)  # type: ignore
    puk1: constr(min_length=8, max_length=8)  # type: ignore
    pin2: constr(min_length=4, max_length=4)  # type: ignore
    puk2: constr(min_length=8, max_length=8)  # type: ignore
    adm1: constr(min_length=8, max_length=8)  # type: ignore
    adm6: constr(min_length=8, max_length=8)  # type: ignore
    acc: constr(min_length=4, max_length=4)  # type: ignore
    size: conint(ge=1, le=1000)  # type: ignore
    prod_check: bool
    elect_check: bool
    graph_check: bool
    server_check: bool
    pin1_fix: bool
    puk1_fix: bool
    pin2_fix: bool
    puk2_fix: bool
    adm1_fix: bool
    adm6_fix: bool


class PATHS(BaseModel):
    TEMPLATE_JSON: str
    INPUT_FILE_PATH: str
    INPUT_CSV: str
    OUTPUT_FILES_DIR: str
    OUTPUT_FILES_LASER_EXT: str


class PARAMETERS(BaseModel):
    server_variables: List[str]
    data_variables: List[str]
    laser_variables: Dict[str, List[str]]


class ConfigData(BaseModel):
    DISP: DISP
    PATHS: PATHS
    PARAMETERS: PARAMETERS


@dataclass
class ConfigHolder:
    DISP: DISP
    PATHS: PATHS
    PARAMETERS: PARAMETERS

    @classmethod
    def from_config(cls, config: ConfigData):
        return cls(DISP=config.DISP, PATHS=config.PATHS, PARAMETERS=config.PARAMETERS)


def json_loader(path: str) -> ConfigHolder:
    with open(path, "r") as f:
        data = json.load(f)
    config = ConfigData(**data)
    config_holder = ConfigHolder.from_config(config)
    return config_holder


# # if __name__ == "__main__":
# config_holder = json_loader(
#     "D:\STC_APP\improvements\security-layer\datageneration\core\settings.json"
# )

# # Load config data
# with open(
#     "D:\STC_APP\improvements\security-layer\datageneration\core\settings.json", "r"
# ) as f:
#     data = json.load(f)
# config = ConfigData(**data)
# config_holder = ConfigHolder.from_config(config)
