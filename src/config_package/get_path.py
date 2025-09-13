# open json file and read data
import os
import json

def get_json_data_path(type):
    abs_root = os.path.abspath(os.path.join(os.getcwd(), "..")) # move to parent of cwd (..), and get the absolute path

    config_path = os.path.join(abs_root, "configs", "config.json") # join root with configs/config.json

    # open config.json file
    with open(config_path, 'r') as file:
        config = json.load(file)

    # using config, get abs paths for data
    data_path = os.path.join(abs_root, config["json_data_dir"], f"{type.lower()}.json")
    return data_path