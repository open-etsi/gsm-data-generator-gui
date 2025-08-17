"""
File Name : FileGenerator.py
Written : 13-09-2023
Description : File include fucntionality for reading zong input file format and store data in json file

Original file is located at
https://colab.research.google.com/drive/1Nz_MGqPs5z1rz_G6NBl8xH-dQJxeK1Z3 : Private
Author : Hamza Qureshi
"""

"""
IMPORTS
"""
import os
import json
import numpy as np
import pandas as pd
from datetime import datetime
from typing import List, Optional
from core.GlobalParams import PARAMETERS, DATA_FRAMES

CONFIGURATION_FILE_PATH = "settings.json"


def read_json(file_path: str):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return dict(data)


# def list_2_str(string,args:Optional[str]=" "):
#     return " ".join(map(str, list(string)))


def list_2_str(lst: List, separator: Optional[str] = " "):
    return separator.join(map(str, lst))


def before_call(another_function):
    def decorator(func):
        def wrapper(self, *args, **kwargs):  # Added 'self' parameter
            another_function(self)  # Call the function passed as an argument
            result = func(self, *args, **kwargs)  # Pass 'self'
            return result

        return wrapper

    return decorator


# def var_call(another_function):
#     def decorator(func):
#         def wrapper(self, *args, **kwargs):
#             another_function(self)  # Call the function passed as an argument
#             result = func(self, *args, **kwargs)
#             return result
#         return wrapper
#     return decorator


class ZongFileWriter:
    """
    ZongFileWriter class representing the interface for handling proactive commands related to Operator Input Files.
    This class returns JSON variables as commands.
    """

    def __init__(self):
        """
        Initialize ZongFileWriter.
        Creates necessary output folders, sets the JSON path, and performs other initialization tasks.
        """
        self._out_graph_path = None
        self._out_elect_path = None
        self._out_server_path = None
        self.seperators = None
        self.output_dir = None
        self.Input_File_Path = None
        self.json_temp = None
        self.template_json = None
        self.parameters = PARAMETERS.get_instance()
        self.dataframes = DATA_FRAMES.get_instance()
        self.json_path = CONFIGURATION_FILE_PATH

    def read_var_from_json(self):
        self.json_temp = read_json(file_path=self.json_path)
        self.Input_File_Path = self.json_temp["PATHS"]["INPUT_FILE_PATH"]
        #        self.Ouput_File_Path_server = self.json_temp["PATHS"]["OUTPUT_SERVER_FILE_PATH"]
        self.output_dir = self.json_temp["PATHS"]["OUTPUT_FILES_DIR"]
        self.seperators = (
            self.json_temp["DISP"]["elect_data_sep"],
            self.json_temp["DISP"]["server_data_sep"],
            self.json_temp["DISP"]["graph_data_sep"],
        )
        self.create_output_folder(self.output_dir)

    def set_json_to_UI(self):
        self.json_path = CONFIGURATION_FILE_PATH
        self.read_var_from_json()
        self.set_file_names()

    def set_json_to_API(self, path: str):
        self.json_path = path
        self.Input_File_Path = path["PATHS"]["INPUT_FILE_PATH"]
        #        self.Ouput_File_Path_server= path["PATHS"]["OUTPUT_SERVER_FILE_PATH"]
        self.output_dir = path["PATHS"]["OUTPUT_FILES_DIR"]
        self.create_output_folder(self.output_dir)
        self.json_temp = path
        self.set_file_names()

    def set_file_names(self):
        header_var_json_path = self.json_temp["PATHS"]["TEMPLATE_JSON"]
        self.template_json = read_json(header_var_json_path)
        job_name = self.template_json["JOB_NAME"]

        self._out_server_path = self.output_dir + "/{}.out".format(job_name)
        self._out_elect_path = self.output_dir + "/DATA_{}.txt".format(job_name)
        self._out_graph_path = self.output_dir + "/LASER_{}.txt".format(job_name)

    @staticmethod
    def create_output_folder(folder_name: str):
        """
        Create an output folder with the given name.

        Args:
            folder_name (str): The name of the folder to create.
        """
        print("Dir to be created is", folder_name)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    @staticmethod
    def generate_dummy_df(var_out: list):
        """
        Create an output dataframe for testing.

        Args:
            var_out (list): The DF with list as header.
        """

        # data = pd.DataFrame()
        data = np.random.randint(
            100000000, 999999999, size=(3, len(var_out))
        )  # Replace 1 and 100 with your desired range
        column_names = [
            "IMSI",
            "ICCID",
            "PIN1",
            "PUK1",
            "PIN2",
            "PUK2",
            "ADM6",
            "ADM1",
            "OPC",
            "KI",
            "ACC",
        ]
        df = pd.DataFrame(data, columns=var_out, column_names=column_names)
        return df

    @staticmethod
    def write_header(output_file_name, zong_output_file_format):
        if True:
            with open(output_file_name, "w", encoding="utf-8") as file:
                file.truncate(0)
                file.write(zong_output_file_format)
            file.close()

    @staticmethod
    def write_df(
        output_file_name,
        df: pd.DataFrame,
        header: bool,
        separator: Optional[str] = " ",
    ):
        df.to_csv(output_file_name, mode="a", index=False, sep=separator, header=header)
        print(f"File '{output_file_name}' has been generated.")

    # ===========================================#
    # ==================FUNC DEF=================#
    # ===========================================#

    @staticmethod
    def header_from_df(df):
        headers = " ".join(map(str, list(df.columns)))
        return headers

    @staticmethod
    def current_time():
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return time_now

    @staticmethod
    def get_imsi_start_end_from_df(df):
        imsi_start = df["IMSI"][0]
        imsi_stop = df["IMSI"][df.shape[0] - 1]
        return [imsi_start, imsi_stop]

    @staticmethod
    def get_iccid_start_end_from_df(df):
        iccid_start = df["ICCID"][0]
        iccid_stop = df["ICCID"][df.shape[0] - 1]
        return [iccid_start, iccid_stop]

    # def read_json(self, file_path: str):
    #     with open(file_path, "r") as json_file:
    #         data = json.load(json_file)
    #     return dict(data)

    def read_json_and_fill_template(self, header1: list, data: dict, in_out_str: str):
        file_name = data[in_out_str]["file_name"]
        vendor = data[in_out_str]["vendor"]
        card_type = data[in_out_str]["card_type"]
        quantity = data[in_out_str]["quantity"]
        local_imsi_from = data[in_out_str]["imsi"][0]
        local_imsi_to = data[in_out_str]["imsi"][1]
        serial_number_icc_id_from = data[in_out_str]["iccid"][0]
        serial_number_icc_id_to = data[in_out_str]["iccid"][1]
        kid = data[in_out_str]["kid"]
        opid = data[in_out_str]["opid"]
        generated_on = self.current_time()
        #        headers = " ".join(map(str, list(header1)))
        #        headers = self.list_2_str(header1)

        zong_output_server_file_format = f"""File Name             : {file_name}
Vendor                : {vendor}
Card Type             : {card_type}
Quantity              : {quantity}
Local IMSI From       : {local_imsi_from}   To : {local_imsi_to}
SERIAL NUMBER/ICC-ID  : {serial_number_icc_id_from}   To : {serial_number_icc_id_to}
KID                   : {kid}
OPID                  : {opid}
Generated on          : {generated_on}
"""
        #        var out:{headers}
        return zong_output_server_file_format

    ####################################################
    # =================WRITE LASER======================#
    ####################################################
    def write_laser_variables(self, x):
        with open(self._out_graph_path, "a", encoding="utf-8") as file:
            #            file.truncate(0)
            var = "varout: " + list_2_str(x, self.seperators[2])
            file.write(var)
            file.write("\n")
            file.close()

    def write_server_variables(self, x):
        with open(self._out_server_path, "a", encoding="utf-8") as file:
            #            file.truncate(0)
            var = "varout: " + list_2_str(x, self.seperators[1])
            file.write(var)
            file.write("\n")
            file.close()

    def write_elect_variables(self, x):
        with open(self._out_elect_path, "a", encoding="utf-8") as file:
            #            file.truncate(0)
            # var = "varout: " + list_2_str(x, self.seperators[0])
            var = list_2_str(x, self.seperators[0])
            file.write(var)
            file.write("\n")
            file.close()

    def write_laser_template(self):
        #        headers_laser = self.json_temp["PARAMETERS"]["laser_variables"]
        zong_output_laser_file_format = self.read_json_and_fill_template(
            header1="", data=self.template_json, in_out_str="input"
        )
        self.write_header(self._out_graph_path, zong_output_laser_file_format)

    #    @before_call(write_laser_template)
    def Generate_laser_file(self, x, df):
        #        self.write_laser_variables(x)

        try:
            self.write_df(self._out_graph_path, df, False, self.seperators[2])
        except Exception as e:
            print("error {}".format(e))

    # ====================================================#
    # =================WRITE SERVER======================#
    # ====================================================#

    def write_server_template(self):
        # header_var_json_path = self.json_temp["PATHS"]["TEMPLATE_JSON"]
        # header_var_json = self.read_json(header_var_json_path)

        #        headers_laser = self.json_temp["PARAMETERS"]["server_variables"]
        zong_output_laser_file_format = self.read_json_and_fill_template(
            header1="", data=self.template_json, in_out_str="input"
        )
        self.write_header(self._out_server_path, zong_output_laser_file_format)

    @before_call(write_server_template)
    def Generate_servr_file(self, x, df):
        self.write_server_variables(x)
        try:
            self.write_df(self._out_server_path, df, False, self.seperators[1])
        except Exception as e:
            print("error {}".format(e))

    #####################################################
    # =================WRITE ELECT=======================#
    #####################################################

    def write_elect_template(self):
        # header_var_json_path = self.json_temp["PATHS"]["TEMPLATE_JSON"]
        # header_var_json = self.read_json(header_var_json_path)

        headers_laser = self.json_temp["PARAMETERS"]["data_variables"]
        zong_output_laser_file_format = self.read_json_and_fill_template(
            header1=headers_laser, data=self.template_json, in_out_str="input"
        )
        self.write_header(self._out_elect_path, zong_output_laser_file_format)

    #    @before_call(write_elect_template)
    def Generate_elect_file(self, x, df=None):
        self.write_elect_variables(x)

        try:
            self.write_df(self._out_elect_path, df, False, self.seperators[0])
        #            self.write_df(self.output_dir + "/elect.txt", df, False)
        except Exception as e:
            print("error {}".format(e))

    def get_output_dir(self) -> str:
        return self.output_dir


# if __name__ == "__main__":
#     m_zong = ZongGenerateHandle()
#     m_zong.get_output_dir()
#     factory_data_json_path=paths["DATA_LASER_PARAM_JSON"]
#     data=m_zong.read_json(factory_data_json_path)
#     headers_server=data["server_variables"]
#     headers_data=data["data_variables"]
#     headers_laser=data["laser_variables"]

#     m_zong=Zong_Generate_Handle()

#     m_zong.Generate_laser_file(True,True)
#     m_zong.Generate_server_file(True,True)
#     m_zong.Generate_elect_file(True,True)
__all__ = ["ZongFileWriter"]
