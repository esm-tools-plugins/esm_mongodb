# -*- coding: utf-8 -*-

"""Main module."""

from loguru import logger
from pymongo import MongoClient
import yaml

from .config import get_config


def _fixup_dict(d):
    new = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = _fixup_dict(v)
        if isinstance(k, str):
            new[k.replace('.', '-')] = v
        else:
            new[k] = v
    return new


def register_simulation(sim_config):
    plugin_config_file = sim_config["general"].get("esm_mongodb_configfile")
    plugin_config = get_config(plugin_config_file)
    opted_in_to_db = sim_config["general"].get("esm_mongodb_use") or plugin_config(
        "use_plugin"
    )
    debug = sim_config["general"].get("esm_mongodb_debug") or plugin_config("debug")
    collection_name = sim_config["general"].get(
        "esm_mongodb_collection_name"
    ) or plugin_config("collection_name")
    if opted_in_to_db:
        host = sim_config["general"].get("esm_mongodb_hostname") or plugin_config("hostname")
        port = sim_config["general"].get("esm_mongodb_port") or plugin_config("port")
        if debug:
            logger.debug(f"Connect to mongodb://{host}:{port}/")
        client = MongoClient(f"mongodb://{host}:{port}/")
        database = client.esm_runs
        if debug:
            logger.debug("All databases:")
            logger.debug(client.list_database_names())
            logger.debug(database)
        collection = database[collection_name]
        logger.info("Inserting sim_config!")
        with open("database_config", "w") as f:
            f.write(yaml.safe_dump(sim_config))
        sim_config = yaml.safe_load(f.name)
        collection.insert_one(_fixup_dict(sim_config))
    return sim_config
