# from typing import List, Dict

# from typing import List, Dict

# # class JSONParameters:
# #     _instance = None

# #     def __new__(cls):
# #         if cls._instance is None:
# #             cls._instance = super(JSONParameters, cls).__new__(cls)
# #             cls._instance.paths = cls.Paths()
# #             cls._instance.variables = cls.Variables()
# #             cls._instance.disp = cls.Disp()
# #         return cls._instance


# #===============================================#
# #===============================================#
# #===============================================#
# #===============================================#
# class OuterSingleton:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(OuterSingleton, cls).__new__(cls)
#             cls._instance.nested_instance = OuterSingleton.NestedSingleton()
#         return cls._instance

#     class NestedSingleton:
#         _instance = None

#         def __new__(cls):
#             if cls._instance is None:
#                 cls._instance = super(OuterSingleton.NestedSingleton, cls).__new__(cls)
#             return cls._instance

# #===============================================#
# #===============================================#
# #===============================================#
# #===============================================#


# class JSONParameters:
#     __instance = None
#     """
#         Class include functionality for reading and writing json file according to different
#         operators, fucntionality for differnt operators maybe added later
#     """

#     def __init__(self):
#         if JSONParameters.__instance is not None:
#             raise Exception(
#                 "JSON_PARAMETERS class is a singleton! Use get_instance() to access the instance."
#             )
#         else:
#             JSONParameters.__instance = self

#     # @staticmethod
#     # def get_instance():
#     #     if JSONParameters.__instance is None:
#     #         JSONParameters.__instance = JSONParameters()
#     #     return JSONParameters.__instance


#     # def __new__(cls):
#     #     if cls.__instance is None:
#     #         cls.__instance = super(JSONParameters, cls).__new__(cls)
#     #         cls.__instance.Paths = cls.Paths()
#     #         cls.__instance.Variables = cls.Variables()
#     #         cls.__instance.Disp = cls.Disp()
#     #     return cls.__instance

#     # @staticmethod
#     # def get_instance():
#     #     if JSONParameters.__instance is None:
#     #         JSONParameters.__instance = JSONParameters()
#     #     return JSONParameters.__instance
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(JSONParameters, cls).__new__(cls)
#             cls._instance.nested_instance = JSONParameters.Paths()
#             cls._instance.nested_instance = JSONParameters.Variables()
#             cls._instance.nested_instance = JSONParameters.Disp()
#         return cls._instance

#     # @staticmethod
#     # def get_instance():
#     #     if JSONParameters.__instance is None:
#     #         JSONParameters.__instance = JSONParameters()
#     #         JSONParameters.__instance.Paths     = JSONParameters.Paths()
#     #         JSONParameters.__instance.Variables = JSONParameters.Variables()
#     #         JSONParameters.__instance.Disp      = JSONParameters.Disp()
#     #     return JSONParameters.__instance

#     class Paths:
#         _instance = None
#         def __new__(cls):
#             if cls._instance is None:
#                 cls._instance = super(JSONParameters.Paths, cls).__new__(cls)
#             return cls._instance

#         def __init__(self) -> None:
#             self.__TEMPLATE_JSON = None
#             self.__INPUT_FILE_PATH = None
#             self.__INPUT_CSV = None
#             self.__OUTPUT_FILES_DIR = None
#             self.__OUTPUT_FILES_LASER_EXT = None
#             pass

#         def set_TEMPLATE_JSON(self, value):
#             self.__TEMPLATE_JSON = str(value)

#         def get_TEMPLATE_JSON(cls) -> str:
#             return cls.__TEMPLATE_JSON

#         def set_INPUT_FILE_PATH(self, value) -> None:
#             self.__INPUT_FILE_PATH = str(value)

#         def get_INPUT_FILE_PATH(self) -> str:
#             return self.__INPUT_FILE_PATH

#         def set_INPUT_CSV(self, value) -> None:
#             self.__INPUT_CSV = str(value)

#         def get_INPUT_CSV(self) -> str:
#             return self.__INPUT_CSV

#         def set_OUTPUT_FILES_DIR(self, value) -> None:
#             self.__OUTPUT_FILES_DIR = str(value)

#         def get_OUTPUT_FILES_DIR(self) -> str:
#             return self.__OUTPUT_FILES_DIR

#         def set_OUTPUT_FILES_LASER_EXT(self, value) -> None:
#             self._PIN2 = str(value)

#         def get_OUTPUT_FILES_LASER_EXT(self) -> str:
#             return self.__OUTPUT_FILES_LASER_EXT

#     class Variables:
#         _instance = None
#         def __new__(cls):
#             if cls._instance is None:
#                 cls._instance = super(JSONParameters.Variables, cls).__new__(cls)
#             return cls._instance

#         """To handle variables section in settings.json
#         """
#         def __init__(self) -> None:
#             self.__LASER_DICT = None
#             self.__SERVER_LIST = None
#             self.__ELECT_LIST = None
#             pass

#         def set_LASER_DICT(self, value: Dict) -> None:
#             self.__LASER_DICT = str(value)

#         def get_LASER_DICT(self) -> Dict:
#             return self.__LASER_DICT

#         def set_SERVER_LIST(self, value: List) -> None:
#             self.__SERVER_LIST = str(value)

#         def get_SERVER_LIST(self) -> List:
#             return self.__SERVER_LIST

#         def set_ELECT_LIST(self, value: List) -> None:
#             self.__ELECT_LIST = str(value)

#         def get_ELECT_LIST(self) -> List:
#             return self.__ELECT_LIST

#     class Disp:
#         _instance = None
#         def __new__(cls):
#             if cls._instance is None:
#                 cls._instance = super(JSONParameters.Disp, cls).__new__(cls)
#             return cls._instance

#         def __init__(self) -> None:
#             """To be added later for display paramerters
#             """
#             pass


# a = JSONParameters.get_instance()
