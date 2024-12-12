# import json
# from typing import Dict, Any

# # from core.exceptions import NoJsonFilePresent
# # from core.GlobalParams import PARAMETERS

# from exceptions import NoJsonFilePresent
# from GlobalParams import PARAMETERS

# CONFIGURATION_FILE_PATH = "./settings.json"


# class JsonHandler(PARAMETERS):
#     def __init__(self) -> None:
#         super().__init__()
#         self.params = PARAMETERS.get_instance()

#     @classmethod
#     def __read_json(
#         cls, file_path: str
#     ) -> dict[Any, Any] | dict[str, Any] | dict[str, str] | None:
#         try:
#             with open(file_path, "r") as json_file:
#                 data = json.load(json_file)
#             return dict(data)
#         except FileNotFoundError:
#             print(f"Error: File '{file_path}' not found.")
#             raise NoJsonFilePresent("Error: File '{file_path}' not found.")
#         except json.JSONDecodeError as e:
#             print(f"Error decoding JSON in '{file_path}': {e}")
#             return (
#                 None  # You can choose to return None or raise a custom exception here
#             )

#     @staticmethod
#     def list_2_dict(list_arg: list) -> dict:
#         dict_var = {}
#         for index in range(0, len(list_arg)):
#             dict_var[str(index)] = [list_arg[index], "Normal", "0-31"]
#         return dict_var

#     @staticmethod
#     def dict_2_list(d: dict) -> list:
#         list1 = []
#         for index, j in enumerate(d):
#             temp = list(d.values())[index][0]
#             list1.append(temp)
#         return list1

#     # def read_paths_for_UI(self):
#     #     data = JsonHandler.__read_json(CONFIGURATION_FILE_PATH)
#     #     if data:
#     #         self.params.set_TEMPLATE_JSON(data["PATHS"]["TEMPLATE_JSON"])
#     #         self.params.set_INPUT_FILE_PATH(data["PATHS"]["INPUT_FILE_PATH"])
#     #         self.params.set_INPUT_CSV(data["PATHS"]["INPUT_CSV"])
#     #         self.params.set_OUTPUT_FILES_DIR(data["PATHS"]["OUTPUT_FILES_DIR"])
#     #         self.params.set_OUTPUT_FILES_LASER_EXT(data["PATHS"]["OUTPUT_FILES_LASER_EXT"])

#     def read_paths(self):
#         data = JsonHandler.__read_json(CONFIGURATION_FILE_PATH)
#         if data:
#             self.params.set_TEMPLATE_JSON(data["PATHS"]["TEMPLATE_JSON"])
#             self.params.set_INPUT_FILE_PATH(data["PATHS"]["INPUT_FILE_PATH"])
#             self.params.set_INPUT_CSV(data["PATHS"]["INPUT_CSV"])
#             self.params.set_OUTPUT_FILES_DIR(data["PATHS"]["OUTPUT_FILES_DIR"])
#             self.params.set_OUTPUT_FILES_LASER_EXT(
#                 data["PATHS"]["OUTPUT_FILES_LASER_EXT"]
#             )

#     def read_variables(self):
#         data = JsonHandler.__read_json(CONFIGURATION_FILE_PATH)
#         if data:
#             self.params.set_ELECT_DICT(
#                 JsonHandler.list_2_dict(data["PARAMETERS"]["data_variables"])
#             )
#             self.params.set_GRAPH_DICT((data["PARAMETERS"]["laser_variables"]))
#             self.params.set_SERVER_DICT(
#                 JsonHandler.list_2_dict(data["PARAMETERS"]["server_variables"])
#             )


# # j = JsonHandler()
# # j.read_paths()
# # j.read_variables()
# # j.__read_json()
