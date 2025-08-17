"""
File Name : FileParser.py
Written : 13-09-2023
Description : File include fucntionality for reading zong input file format and store data in json file

Original file is located at
https://colab.research.google.com/drive/1Nz_MGqPs5z1rz_G6NBl8xH-dQJxeK1Z3 : Private
Author : Hamza Qureshi

"""

"""IMPORTS"""

import re
import os
import json
import pandas as pd

# from datetime import datetime
import datetime as datetime

# ====================#
# ====================#
# ====================#

CONFIGURATION_FILE_PATH = "settings.json"

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


paths = read_json(file_path=CONFIGURATION_FILE_PATH)

if paths:
    Input_File_Path = paths["PATHS"]["INPUT_FILE_PATH"]
    template_json = paths["PATHS"]["TEMPLATE_JSON"]
    Input_DataFrame = paths["PATHS"]["INPUT_CSV"]
# Ouput_File_Path_server = paths["PATHS"]["OUTPUT_SERVER_FILE_PATH"]
# Ouput_File_Path_laser= OUTPUT_LASER_FILE_PATH
# Ouput_File_Path_data=OUTPUT_DATA_FILE_PATH
# ==================== #
# ==================== #
# ==================== #
# input_json=paths["INPUT_JSON"]
# output_server_json=paths["SERVER_JSON"]
# template_json = paths["PATHS"]["TEMPLATE_JSON"]

# ====================#
# ====================#
# ====================#


class ZongFileParser:
    """
    ZongFileParser class representing the interface of some code that handles
    the proactive commands related to Operator Input Files, as it return json variables command.
    """

    def __init__(self, input_path) -> None:
        self.create_output_folder(
            "operators/zong"
        )  # create required folers for safe side
        f = open("operators/zong/template.json", "w+", encoding="utf-8")
        # creating file
        self.path = input_path
        pass

    def create_output_folder(self, folder_name: str):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    def open_file(self, path: str, no_of_lines_read: int = 50):
        with open(path, "r", encoding="utf-8") as file:
            file_contents = file.readlines()[0:no_of_lines_read]
        return file_contents

    def read_df(self, path: str, skip_lines: int, sep: str):
        try:
            return pd.read_csv(
                path, sep=sep, skiprows=skip_lines, header=None, engine="python"
            )
        except pd.errors.EmptyDataError:
            print("The file is empty.")
        except pd.errors.ParserError:
            print("The file is not a pandas DataFrame.")

    def for_list_var(self, regex: str, line: str) -> list:
        match = re.search(regex, line, re.UNICODE)
        if match is not None:
            result = match.group().replace("\n", "").replace(":", "").split(" ")
            return result
        else:
            return ["", ""]  # default

    def for_double_var(self, regex: str, line: str) -> list:
        Local_IMSI_From_data = re.finditer(regex, line, re.UNICODE)
        result = []
        for data in Local_IMSI_From_data:
            result.append(data.group().replace("-", ""))
        return result

    def for_single_var(self, regex: str, line: str):
        match = re.search(regex, line, re.UNICODE)
        if match is not None:
            return (
                match.group()
                .replace("\n", "")
                .replace(":", "")
                .replace(" ", " ")
                .lstrip(" ")
            )
        else:
            return []

    def input_file_2_json(self, input_file_patterns, content):
        variables = {}
        for line in range(0, len(input_file_patterns)):
            pattern = list(input_file_patterns.values())[line][2]
            function_name = list(input_file_patterns.values())[line][0]
            validity = list(input_file_patterns.values())[line][1]
            key = list(input_file_patterns.keys())[line]
            if validity == "valid":
                if function_name == "single":
                    variables[key] = self.for_single_var(pattern, content[line])
                else:
                    variables[key] = self.for_double_var(pattern, content[line])
            elif validity == "dataframe":
                #            pd.read_csv()
                pass
            else:
                pass
        return {"input": variables}

    #        return variables

    def ouput_file_2_json(self, input_file_patterns, content):
        variables = {}
        for line in range(0, len(input_file_patterns)):
            pattern = list(input_file_patterns.values())[line][2]
            function_name = list(input_file_patterns.values())[line][0]
            validity = list(input_file_patterns.values())[line][1]
            key = list(input_file_patterns.keys())[line]
            if validity == "valid":
                if function_name == "single":
                    variables[key] = self.for_single_var(pattern, content[line])
                elif function_name == "double":
                    variables[key] = self.for_double_var(pattern, content[line])
                elif function_name == "list":
                    variables[key] = self.for_list_var(pattern, content[line])
            elif validity == "dataframe":
                # read df from here
                pass
            else:
                pass
        #        return variables

        return {"output": variables}

    # def write_output_file(self, path: str, variables: dict):
    #     with open(path, "w+", encoding="utf-8") as file:
    #         try:
    #             data = json.load(file)  # Read the existing JSON data
    #         except json.JSONDecodeError:
    #             print("EEEERRRRRRRRROOOOOOOOOOOORRRRRRRRRRR!!!!!")
    #             data = (
    #                 {}
    #             )  # Initialize with an empty dictionary if the file is empty or invalid JSON

    #         # Update or create the input and output objects as needed
    #         data["output"] = variables.get("output", {})

    #         # Move the file cursor back to the beginning to overwrite the file
    #         file.seek(0)

    #         # Write the updated data back to the file
    #         json.dump(data, file, indent=4)

    #         # Truncate any remaining content (in case the new data is shorter than the old data)
    #         file.truncate()

    def write_input_file_json(self, path: str, variables: dict):
        #    path=os.path.join(os.getcwd(),path)

        with open(path, "r+", encoding="utf-8") as file:
            try:
                data = json.load(file)  # Read the existing JSON data
            except json.JSONDecodeError as e:
                print("ERROR!", e)
                data = {}  # Initialize with an empty dictionary if the file is empty or invalid JSON
            #            data={}
            # Update or create the input and output objects as needed
            data["input"] = variables.get("input", {})

            # Move the file cursor back to the beginning to overwrite the file
            file.seek(0)

            # Write the updated data back to the file
            json.dump(data, file, indent=4)

            # Truncate any remaining content (in case the new data is shorter than the old data)
            file.truncate()

    def write_input_file_Name(self, path: str, variables: dict):
        with open(path, "r+", encoding="utf-8") as file:
            try:
                data = json.load(file)  # Read the existing JSON data
            except json.JSONDecodeError:
                data = {}  # Initialize with an empty dictionary if the file is empty or invalid JSON

            # Update or create the input and output objects as needed
            data["JOB_NAME"] = variables.get("JOB_NAME", {})

            # Move the file cursor back to the beginning to overwrite the file
            file.seek(0)

            # Write the updated data back to the file
            json.dump(data, file, indent=4)

            # Truncate any remaining content (in case the new data is shorter than the old data)
            file.truncate()

    def input_file_handle(self):
        # read input file MNO and generate config json
        try:
            content = self.open_file(self.path, no_of_lines_read=11)
            var = self.input_file_2_json(
                input_file_patterns=input_file_patterns, content=content
            )
            self.write_input_file_json(template_json, var)
            file_name = os.path.splitext(os.path.basename(self.path))[0]

            #            file_name = os.path.basename(self.path)
            var = {"JOB_NAME": file_name}
            self.write_input_file_Name(template_json, var)

            # read dataframe and sore in csv file fro temp
            dataframe = self.read_df(self.path, 12, "\t\t")
            dataframe.columns = ["ICCID", "IMSI"]
            dataframe.to_csv(Input_DataFrame, header=True, index=False)
            # print(dataframe)
            return dataframe

        except Exception as e:
            print("Error!", e)

    # def output_file_handle(self):
    #     # read input file MNO server and generate config json
    #     try:
    #         content = self.open_file(self.path, no_of_lines_read=10)
    #         var = self.ouput_file_2_json(
    #             input_file_patterns=output_file_patterns, content=content
    #         )
    #         self.write_output_file(template_json, var)
    #         # self.write_file(output_server_json,variables=var)
    #     except Exception as e:
    #         print("Error!", e)


output_file_patterns = {
    #   Variable Name           No of Values to Get     Respective Regex
    "file_name": ["single", "valid", r":\s*([^:]+)"],  # 1
    "vendor": ["single", "valid", r":\s*([^:]+)"],  # 2
    "card_type": ["single", "valid", r":\s*([^:]+)"],  # 3
    "quantity": ["single", "valid", r":\s*([^:]+)"],  # 4
    "imsi": ["double", "valid", r"((4100)[0-9]{11})"],  # 5
    "iccid": ["double", "valid", r"((899)[0-9]{15})"],  # 6
    "kid": ["single", "valid", r":\s*([^:]+)"],  # 7
    "opid": ["single", "valid", r":\s*([^:]+)"],  # 8
    "generated_on": ["single", "valid", r":\s*([^:]+)"],  # 9
    "var_out": ["list", "valid", r":\s*([^:]+)"],  # 10
}

# ========================================================#
# =======================READ VARS========================#
# ========================================================#

input_file_patterns = {
    #   Variable Name           No of Values to Get     Respective Regex
    "file_name": ["single", "valid", r":\s*([^:]+)"],  # 1
    "vendor": ["single", "valid", r":\s*([^:]+)"],  # 2
    "card_type": ["single", "valid", r":\s*([^:]+)"],  # 3
    "quantity": ["single", "valid", r":\s*([^:]+)"],  # 4
    "imsi": ["double", "valid", r"((4100)[0-9]{11})"],  # 5
    "iccid": ["double", "valid", r"((899)[0-9]{15})"],  # 6
    "kid": ["single", "valid", r":\s*([^:]+)"],  # 7
    "opid": ["single", "valid", r":\s*([^:]+)"],  # 8
    "generated_on": ["single", "valid", r":\s*([^:]+)"],  # 9
    "1": ["single", "Invalid", r":\s*([^:]+)"],  # 10
    "variables": ["double", "valid", r"(\bIMSI\b|\bICC-ID\b)"],  # 11
    "2": ["single", "Invalid", r":\s*([^:]+)"],  # 12
}


# if __name__ == "__main__":
#     try:
#         m_zong = ZongReaderHandle(Input_File_Path)
#         m_zong.input_file_handle()
#         del m_zong

#         # m_zong = Zong_Read_Handle(Ouput_File_Path_server)
#         # m_zong.output_file_handle()
#         # del m_zong

#     except NameError as e:
#         print("NameError!", e)


__all__ = ["ZongFileParser"]
