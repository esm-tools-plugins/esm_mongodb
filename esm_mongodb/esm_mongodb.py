# -*- coding: utf-8 -*-

"""Main module."""

from loguru import logger
from pymongo import MongoClient

from .config import get_config


def register_simulation(sim_config):
    plugin_config_file = sim_config.get("esm_mongodb_configfile")
    plugin_config = get_config(plugin_config_file)
    opted_in_to_db = sim_config.get("esm_mongodb_use") or plugin_config("use_plugin")
    debug = sim_config.get("esm_mongodb_debug") or plugin_config("debug")
    collection_name = sim_config.get("esm_mongodb_collection_name") or plug_config("collection_name")
    if opted_in_to_db:
        host = sim_config.get("esm_mongodb_hostname") or plugin_config("hostname")
        port = sim_config.get("esm_mongodb_port") or plugin_config("port")
        if debug:
            logger.debug(f"Connect to mongodb://{host}:{port}/")
        client = MongoClient(f"mongodb://{host}:{port}/")
        database = client.esm_runs
        if debug:
            logger.debug("All databases:")
            logger.debug(client.list_database_names())
            logger.debug(database)
        collection = database[collection_name]
        collection.insert_one(sim_config)
    return sim_config
