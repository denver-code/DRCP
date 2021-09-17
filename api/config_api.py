import configparser
import codecs
import json


def get_value(name, filep="config", ctype="Default"):
    config = configparser.ConfigParser()
    config.read_file(codecs.open(f"{filep}.ini", "r", "utf8"))
    return config[ctype][name]

def get_bool(name, filep="config", ctype="Default"):
    config = configparser.ConfigParser()
    config.read_file(codecs.open(f"{filep}.ini", "r", "utf8"))
    return config.getboolean(ctype, name)

def get_array(name, filep="config", ctype="Default"):
    config = configparser.ConfigParser()
    config.read_file(codecs.open(f"{filep}.ini", "r", "utf8"))
    return json.loads(config[ctype][name])

def set_value(name, value, filep="config", ctype="Default"):
    config = configparser.ConfigParser()
    config.read_file(codecs.open(f"{filep}.ini", "r", "utf8"))
    config[ctype][name] = value
    with codecs.open(f"{filep}.ini", "w", "utf8") as configfile:
        config.write(configfile)

def get_key_list(filep):
    config = configparser.ConfigParser()
    config.read_file(codecs.open(f"{filep}.ini", "r", "utf8"))
    k_list = []
    for i in config:
        for j in config[i]:
            if j is not None:
                k_list.append([i, j])
    return k_list


def get_value_list(filep):
    config = configparser.ConfigParser()
    config.read_file(codecs.open(f"{filep}.ini", "r", "utf8"))
    v_list = []
    for i in config:
        for j in config[i]:
            if j is not None:
                v_list.append([j, config[i][j]])
    return v_list
