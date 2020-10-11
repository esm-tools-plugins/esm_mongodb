#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `esm_mongodb` package."""


import unittest
import os

from esm_mongodb import esm_mongodb
from esm_mongodb.config import get_config

# Test requirement:
import yaml

example_config = {"esm_mongodb_use": True, "esm_mongodb_debug": True, "foo": "bar", "esm_mongodb_collection_name": "ci_tests"}

class TestPluginConfig(unittest.TestCase):
    def test_get_config(self):
        plugin_config = get_config()
        hostname = plugin_config("hostname")
        self.assertEqual(hostname, "paleosrv3.dmawi.de")


class TestEsm_mongodb(unittest.TestCase):
    """Tests for `esm_mongodb` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        with open("esm_tools.yaml", "w") as f:
            f.write(yaml.dump(example_config))

    def tearDown(self):
        """Tear down test fixtures, if any."""
        os.remove("esm_tools.yaml")

    def test_insert(self):
        esm_mongodb.register_simulation(example_config)

    def test_with_real_config(self):
        pass
