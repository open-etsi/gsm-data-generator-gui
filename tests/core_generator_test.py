
from core.generator.script import DataGenerationScript
from core.json_utils import JsonHandler


s = DataGenerationScript()
j = JsonHandler()
factory_data_json_path = "settings.json"
j.read_paths(factory_data_json_path)
j.read_variables()
s.SET_ALL_DISP_PARAMS()  # testing
s.SET_HEADERS()

# (
#     s.dataframes.__ELECT_DF,
#     s.dataframes.__GRAPH_DF,
#     #    s.dataframes.__SERVR_DF,
#     #    s.dataframes.__KEYS,
# ) = s.generate_all_data()

(dfs, keys) = s.generate_all_data()


# print(s.generate_all_data())
# print(dfs["ELECT"])
# print(dfs["GRAPH"])
print(dfs["SERVER"])
# print(keys)
# print(s.dataframes.__SERVR_DF)
