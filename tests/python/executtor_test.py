from gsm_data_generator.executor import DataGenerationScript
from gsm_data_generator.parser import ConfigHolder, json_loader, json_loader1

if __name__ == "__main__":
    config_holder: ConfigHolder = json_loader(
        "C:/Users/DELL/Desktop/datadecryption_poetry/settings.json"
    )
    print(config_holder)
    s = DataGenerationScript(config_holder=config_holder)

    s.json_to_global_params()  # testing
    (dfs, keys) = s.generate_all_data()

    # print(s.generate_all_data())
    print(dfs["ELECT"].to_csv("aaa.csv", index=False))
    print(dfs["GRAPH"].to_csv("bbb.csv", index=False))
    # print(dfs["SERVER"])
