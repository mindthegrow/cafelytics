import pandas as pd
import yaml


def readData(filePath: str):
    """
    Takes a filepath in the form of a string (e.g. 'data/demoData.csv')
    that represents a spreadsheet and returns a pandas dataframe.
    """
    pathExt = filePath.split(".")
    ext = pathExt[1]

    if ext == "csv":
        data = pd.read_csv(filePath)
    elif (ext == "xlsx") or (ext == "xls") or (ext == "xlsm") or (ext == "xlsb"):
        # sheet = input("Please enter the sheet name or number (first sheet = 0, second = 1, etc.)")
        data = pd.read_excel(filePath)

    return data


def openYaml(yamlFilePath: str) -> dict:
    """
    Arguments: filepath str from pwd

    Returns: dictionary with the information contained in the YAML file

    Opens a .yaml/.yml file and returns a dictionary

    """
    yamlFile = open(yamlFilePath)
    parsed = yaml.load(yamlFile, Loader=yaml.FullLoader)
    return parsed
