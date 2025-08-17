import pandas as pd
from typing import Any

debug = False


class DataFrames:
    __instance = None

    def __init__(self):
        if DataFrames.__instance is not None:
            raise Exception(
                "GlobalParameters class is a singleton! Use get_instance() to access the instance."
            )
        else:
            DataFrames.__instance = self
            self.__INPUT_DF = pd.DataFrame()
            self.ELECT_DF = pd.DataFrame()
            self.GRAPH_DF = pd.DataFrame()
            self.SERVER_DF = pd.DataFrame()
            self.__KEYS = {}

    @staticmethod
    def get_instance():
        if DataFrames.__instance is None:
            DataFrames.__instance = DataFrames()
        return DataFrames.__instance

    def set_ELECT_DF(self, value):
        self.ELECT_DF = pd.DataFrame()
        self.ELECT_DF = value

    def get_ELECT_DF(self):
        return self.ELECT_DF

    def set_GRAPH_DF(self, value):
        self.GRAPH_DF = pd.DataFrame()
        self.GRAPH_DF = value

    def get_GRAPH_DF(self):
        return self.GRAPH_DF

    def set_SERVER_DF(self, value):
        self.SERVER_DF = pd.DataFrame()
        self.SERVER_DF = value

    def get_SERVER_DF(self):
        return self.SERVER_DF

    def set_KEYS(self, value):
        self.__KEYS = value

    def get_KEYS(self):
        return self.__KEYS

    def set_input_df(self, value):
        self.__INPUT_DF = pd.DataFrame()
        self.__INPUT_DF = value

    def get_input_df(self):
        return self.__INPUT_DF

    # def is_VALID_DF(self, param, param_name: str) -> bool:
    #     if param_name == "DF":
    #         return param.empty
    #     else:
    #         return False


class Parameters(DataFrames):
    __instance = None

    def __init__(self):
        super().__init__()
        self.__def_head = None
        self.EXTRCATOR_DICT = None
        self.__EXTRACTOR_DICT = None
        if Parameters.__instance is not None:
            raise Exception(
                "GlobalParameters class is a singleton! Use get_instance() to access the instance."
            )
        else:
            Parameters.__instance = self
            self.__ICCID = ""
            self.__IMSI = ""
            self.__PIN1 = ""
            self.__PUK1 = ""
            self.__PIN2 = ""
            self.__PUK2 = ""
            self.__K4 = ""
            self.__OP = ""
            self.__ADM1 = ""
            self.__ADM6 = ""
            self.__ACC = ""
            self.__DATA_SIZE = ""
            self.__ELECT_CHECK = False
            self.__GRAPH_CHECK = False
            self.__SERVER_CHECK = False
            self.__PROD_CHECK = False

            self.__pin1_rand = True
            self.__puk1_rand = True
            self.__pin2_rand = True
            self.__puk2_rand = True
            self.__adm1_rand = True
            self.__adm6_rand = True
            self.__acc_rand = True

            self.__INPUT_PATH = ""
            self.__LASER_EXT_PATH = ""

            self.__ELECT_DICT = {}
            self.__GRAPH_DICT = {}
            self.__SERVER_DICT = {}

            self.__INPUT_FILE_PARAMETERS = {}
            # self.file_name: str
            # ===========================-=================#
            # ================= SEPERATOR==================#
            # =============================================#

            self.__ELECT_SEP: Any = None
            self.__GRAPH_SEP: Any = None
            self.__SERVR_SEP: Any = None

            # ============================================#
            # =================EXTRACTOR==================#
            # ============================================#

            self.__TEMPLATE_JSON: Any = None
            self.__INPUT_FILE_PATH: Any = None
            self.__INPUT_CSV: Any = None
            self.__OUTPUT_FILES_DIR: Any = None
            self.__OUTPUT_FILES_LASER_EXT: Any = None
            self.file_name: Any = None

    #           self.__LASER_DICT = None
    #           self.__SERVER_LIST = None
    #           self.__ELECT_LIST = None
    #           pass

    @staticmethod
    def get_instance():
        if Parameters.__instance is None:
            Parameters.__instance = Parameters()
        return Parameters.__instance

    def set_ELECT_SEP(self, value: str) -> None:
        self.__ELECT_SEP = str(value)

    def get_ELECT_SEP(self) -> str:
        return self.__ELECT_SEP

    def set_GRAPH_SEP(self, value: str) -> None:
        self.__GRAPH_SEP = str(value)

    def get_GRAPH_SEP(self) -> str:
        return self.__GRAPH_SEP

    def set_SERVER_SEP(self, value: str) -> None:
        self.__SERVR_SEP = str(value)

    def get_SERVER_SEP(self) -> str:
        return self.__SERVR_SEP

    def set_TEMPLATE_JSON(self, value):
        self.__TEMPLATE_JSON = str(value)

    def get_TEMPLATE_JSON(self) -> str:
        return self.__TEMPLATE_JSON

    def set_INPUT_FILE_PATH(self, value) -> None:
        self.__INPUT_FILE_PATH = str(value)

    def get_INPUT_FILE_PATH(self) -> str:
        return self.__INPUT_FILE_PATH

    def set_INPUT_CSV(self, value) -> None:
        self.__INPUT_CSV = str(value)

    def get_INPUT_CSV(self) -> str:
        return self.__INPUT_CSV

    def set_OUTPUT_FILES_DIR(self, value) -> None:
        self.__OUTPUT_FILES_DIR = str(value)

    def get_OUTPUT_FILES_DIR(self) -> str:
        return self.__OUTPUT_FILES_DIR

    def set_OUTPUT_FILES_LASER_EXT(self, value) -> None:
        self.__PIN2 = str(value)

    def get_OUTPUT_FILES_LASER_EXT(self) -> str:
        return self.__OUTPUT_FILES_LASER_EXT

    def set_ICCID(self, value):
        self.__ICCID = str(value)

    def set_IMSI(self, value):
        self.__IMSI = str(value)

    def set_PIN1(self, value):
        self.__PIN1 = str(value)

    def set_PUK1(self, value):
        self.__PUK1 = str(value)

    def set_PIN2(self, value):
        self.__PIN2 = str(value)

    def set_PUK2(self, value):
        self.__PUK2 = str(value)

    def set_OP(self, value):
        self.__OP = str(value)

    def set_K4(self, value):
        self.__K4 = str(value)

    def set_ADM1(self, value):
        self.__ADM1 = str(value)

    def set_ADM6(self, value):
        self.__ADM6 = str(value)

    def set_ACC(self, value):
        self.__ACC = str(value)

    def set_DATA_SIZE(self, value):
        self.__DATA_SIZE = str(value)

    def set_ELECT_CHECK(self, value: bool):
        self.__ELECT_CHECK = value

    def set_GRAPH_CHECK(self, value: bool):
        self.__GRAPH_CHECK = value

    def set_SERVER_CHECK(self, value: bool):
        self.__SERVER_CHECK = value

    def set_PRODUCTION_CHECK(self, value: bool):
        self.__PROD_CHECK = not value

    def set_DEFAULT_HEADER(self, value: list):
        self.__def_head = value

    def get_ICCID(self):
        return self.__ICCID

    def get_IMSI(self):
        return self.__IMSI

    def get_PIN1(self):
        return self.__PIN1

    def get_PUK1(self):
        return self.__PUK1

    def get_PIN2(self):
        return self.__PIN2

    def get_PUK2(self):
        return self.__PUK2

    def get_OP(self):
        return self.__OP

    def get_K4(self):
        return self.__K4

    def get_ADM1(self):
        return self.__ADM1

    def get_ADM6(self):
        return self.__ADM6

    def get_ACC(self):
        return self.__ACC

    def get_ELECT_CHECK(self):
        return self.__ELECT_CHECK

    def get_GRAPH_CHECK(self):
        return self.__GRAPH_CHECK

    def get_SERVER_CHECK(self):
        return self.__SERVER_CHECK

    def get_PRODUCTION_CHECK(self):
        return self.__PROD_CHECK

    def get_DATA_SIZE(self):
        return self.__DATA_SIZE

    def get_DEFAULT_HEADER(self):
        return self.__def_head

    def set_PIN1_RAND(self, value: bool):
        self.__pin1_rand = value

    def get_PIN1_RAND(self):
        return self.__pin1_rand

    def set_PUK1_RAND(self, value: bool):
        self.__puk1_rand = value

    def get_PUK1_RAND(self):
        return self.__puk1_rand

    def set_PIN2_RAND(self, value: bool):
        self.__pin2_rand = value

    def get_PIN2_RAND(self):
        return self.__pin2_rand

    def set_PUK2_RAND(self, value: bool):
        self.__puk2_rand = value

    def get_PUK2_RAND(self):
        return self.__puk2_rand

    def set_ADM1_RAND(self, value: bool):
        self.__adm1_rand = value

    def get_ADM1_RAND(self):
        return self.__adm1_rand

    def set_ADM6_RAND(self, value: bool):
        self.__adm6_rand = value

    def get_ADM6_RAND(self):
        return self.__adm6_rand

    def set_ACC_RAND(self, value: bool):
        self.__acc_rand = value

    def get_ACC_RAND(self):
        return self.__acc_rand

    def set_INPUT_PATH(self, value: str):
        self.__INPUT_PATH = value

    def get_INPUT_PATH(self):
        return self.__INPUT_PATH

    def set_LASER_EXT_PATH(self, value: str):
        self.__LASER_EXT_PATH = value

    def get_LASER_EXT_PATH(self):
        return self.__LASER_EXT_PATH

    def set_ELECT_DICT(self, value: dict):
        self.__ELECT_DICT = value

    def get_ELECT_DICT(self):
        return self.__ELECT_DICT

    def set_GRAPH_DICT(self, value: dict):
        self.__GRAPH_DICT = value

    def get_GRAPH_DICT(self):
        return self.__GRAPH_DICT

    def set_SERVER_DICT(self, value: dict):
        self.__SERVER_DICT = value

    def get_SERVER_DICT(self):
        return self.__SERVER_DICT

    def set_INPUT_FILE_PARAMETERS(self, value: dict):
        self.__INPUT_FILE_PARAMETERS = value

    def get_INPUT_FILE_PARAMETERS(self):
        return self.__INPUT_FILE_PARAMETERS

    def set_EXTRACTOR_DICT(self, value: dict):
        self.__EXTRACTOR_DICT = value

    def get_EXTRACTOR_DICT(self):
        return self.EXTRCATOR_DICT

    def set_file_name(self, value: str):
        self.file_name = value

    def get_file_name(self) -> str:
        return self.file_name

    def get_all_params_dict(self) -> dict:
        param_dict = {
            "Demo Data": self.get_PRODUCTION_CHECK(),
            "OP": self.get_OP(),
            "K4": self.get_K4(),
            "ICCID": self.get_ICCID(),
            "IMSI": self.get_IMSI(),
            "PIN1": self.get_PIN1(),
            "PUK1": self.get_PUK1(),
            "PIN2": self.get_PIN2(),
            "PUK2": self.get_PUK2(),
            "ADM1": self.get_ADM1(),
            "ADM6": self.get_ADM6(),
            "ACC": self.get_ACC(),
            "DATA_SIZE": self.get_DATA_SIZE(),
            "INPUT_PATH": self.get_INPUT_PATH(),
        }
        print(param_dict)
        return param_dict

    @staticmethod
    def is_valid(param1, param_name: str):
        result = False
        param = param1
        match param_name:
            case "ICCID":
                result = (
                    len(str(param)) == 20
                    or len(str(param)) == 19
                    or len(str(param)) == 18
                )
            case "IMSI":
                result = len(str(param)) == 15
            case "PIN1" | "PIN2":
                result = len(str(param)) == 4
            case "PUK1" | "PUK2" | "ADM1" | "ADM6":
                result = len(str(param)) == 8
            case "OP":
                result = len(str(param)) == 32
            case "K4":
                result = len(str(param)) == 64
            case "SIZE":
                param = int(param)
                result = len(str(param)) != 0 or param > 0
            case "DICT":
                param = dict(param)
                result = len(param) > 0
        print(param_name, result)
        return result

    @staticmethod
    def is_valid_df(param, param_name: str) -> bool:
        match param_name:
            case "DF":
                df = pd.DataFrame(param)
                return df.empty
            case _:
                return False

    def check_params(self) -> bool:
        if not self.get_PRODUCTION_CHECK():
            print("===============Production===============")
            result = (
                #                self.is_valid(self.get_IMSI(), "IMSI")
                #                and self.is_valid(self.get_ICCID(), "ICCID")
                self.is_valid(self.get_PIN1(), "PIN1")
                and self.is_valid(self.get_PUK1(), "PUK1")
                and self.is_valid(self.get_PIN2(), "PIN2")
                and self.is_valid(self.get_PUK2(), "PUK2")
                and self.is_valid(self.get_ADM1(), "ADM1")
                and self.is_valid(self.get_ADM6(), "ADM6")
                and self.is_valid(self.get_OP(), "OP")
                and self.is_valid(self.get_K4(), "K4")
                #                and self.is_valid(self.get_DATA_SIZE(), "SIZE")
                and self.is_valid(self.get_ELECT_DICT(), "DICT")
                and self.is_valid(self.get_GRAPH_DICT(), "DICT")
            )
        else:
            print("=================Demo===================")
            result = (
                self.is_valid(self.get_IMSI(), "IMSI")
                and self.is_valid(self.get_ICCID(), "ICCID")
                and self.is_valid(self.get_DATA_SIZE(), "SIZE")
                and self.is_valid(self.get_PIN1(), "PIN1")
                and self.is_valid(self.get_PUK1(), "PUK1")
                and self.is_valid(self.get_PIN2(), "PIN2")
                and self.is_valid(self.get_PUK2(), "PUK2")
                and self.is_valid(self.get_ADM1(), "ADM1")
                and self.is_valid(self.get_ADM6(), "ADM6")
                and self.is_valid(self.get_OP(), "OP")
                and self.is_valid(self.get_K4(), "K4")
                and self.is_valid(self.get_ELECT_DICT(), "DICT")
                and self.is_valid(self.get_GRAPH_DICT(), "DICT")
                # self.is_VALID_DF(self.get_ELECT_DF,"DF")
            )
        return result

    def print_all_global_parameters(self):
        print("PIN1", self.get_PIN1())
        print("PIN2", self.get_PIN2())
        print("PIN2", self.get_PIN2())
        print("DATA SIZE", self.get_DATA_SIZE())


__all__ = ["Parameters", "DataFrames"]
