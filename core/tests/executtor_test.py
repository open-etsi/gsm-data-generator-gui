
from core.executor.script import DataGenerationScript
from core.parser.utils import ConfigHolder, json_loader

if __name__ == "__main__":
    config_holder: ConfigHolder = json_loader("C:/Users/DELL/Desktop/datadecryption_poetry/core/settings.json")
    s = DataGenerationScript(config_holder=config_holder)
    s.SET_ALL_DISP_PARAMS()  # testing
    (dfs, keys) = s.generate_all_data()

    # print(s.generate_all_data())
    print(dfs["ELECT"])
    # print(dfs["GRAPH"])
    # print(dfs["SERVER"])
