#!/usr/bin/env python3
"""
Namelist Diff Configuration
===========================

Configuration for the namelist diff tool follows the XDG standard. The
configuration should be stored in a YAML file.

You can use the function write_default_config to generate a configuration file
with the hard-coded defaults. Command line access for this command is available
via::

    $ nmldiff --write-default-config

The default configuration will be written to
``${XDG_CONFIG_HOME}/nmldiff/nmldiff.yaml``

Order of Precedence
-------------------

Configuration is loaded in the following order:

   1. Command line
   2. Config file thats name is declared on the command line.
   3. Environment vars
   4. Local config file (if exists)
   5. Global config file (if exists)
   6. Hard-coded defaults in the code
"""
import getpass

from everett.component import RequiredConfigMixin, ConfigOptions
from everett.ext.yamlfile import ConfigYamlEnv
from everett.manager import ConfigManager, ConfigOSEnv
import xdg.BaseDirectory


CONFIG_FILES = [
    directory + "/esm_tools/esm_tools.yml"
    for directory in xdg.BaseDirectory.xdg_config_dirs
]
"""
List of files where configuration information is searched for
"""


class EsmMongoDBConfig(RequiredConfigMixin):
    """Contains the defaults for the nmldiff configuration"""

    required_config = ConfigOptions()
    required_config.add_option(
        "use_plugin",
        parser=bool,
        default="false",
        doc="Use the MongoDB Plugin",
        namespace="esm_mongodb",
    )
    required_config.add_option(
        "debug",
        parser=bool,
        default="false",
        doc="Switch debug mode on and off.",
        namespace="esm_mongodb",
    )

    required_config.add_option(
        "hostname",
        parser=str,
        default="paleosrv3.dmawi.de",
        doc="Hostname for MongoDB",
        namespace="esm_mongodb",
    )

    required_config.add_option(
        "port",
        parser=str,
        default="27017",
        doc="Port Number for MongoDB",
        namespace="esm_mongodb",
    )

    required_config.add_option(
        "collection_name",
        parser=str,
        default=getpass.getuser(),
        doc="Collection Name (table) to insert into. Defaults to your username",
        namespace="esm_mongodb",
    )


def get_config(config_file=None):
    """Loads the configuration

    Loads either the user supplied configuration, the configuration in the XDG
    path, or the default config. Configuration may be given incompletely, so if
    you only supply the color (for example), other configuration values are
    taken from the defaults. The user can also supply a configuration as a
    dictionary as an argument to this function, this takes first priority.

    Parameters
    ----------
    config_file : str or Path
        Which config to load

    Returns
    -------
    config : dict
        The configuration to use

    Example
    -------

    >>> config = get_config()
    >>> debug = config("debug")  # Evaluates to whatever debug is set in
                                 # the first configuration found
    """

    environments = [
        # Look in OS process environment first
        ConfigOSEnv(),
        # Look in YAML files in order specified
        ConfigYamlEnv(CONFIG_FILES),
    ]
    if config_file:
        environments.insert(0, config_file)
    manager = ConfigManager(
        # Specify one or more configuration environments in
        # the order they should be checked
        environments=environments,
        # Provide users a link to documentation for when they hit
        # configuration errors
        doc="Check https://example.com/configuration for docs.",
    )

    # Apply the configuration class to the configuration manager
    # so that it handles option properties like defaults, parsers,
    # documentation, and so on.
    return manager.with_options(EsmMongoDBConfig())
