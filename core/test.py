
from core.parser.utils import ConfigHolder, json_loader
from core.executor.script import DataGenerationScript

if __name__ == "__main__":
    config_holder: ConfigHolder = json_loader("settings.json")
    s = DataGenerationScript(config_holder=config_holder)
    s.SET_ALL_DISP_PARAMS()  # testing
    (dfs, keys) = s.generate_all_data()

    print(dfs["ELECT"].to_csv("temp_elect.csv"))
    print(dfs["GRAPH"].to_csv("temp_graph.csv"))
    print(dfs["SERVER"].to_csv("temp_server.csv"))



