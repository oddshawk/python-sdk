"""Tests for the public surface the package root declares."""

import oddshawk_sdk
from oddshawk_sdk import hashing as hashing_mod
from oddshawk_sdk import rest as rest_mod


def test_the_package_root_declares_exactly_the_client_and_the_signature_helper():
    assert oddshawk_sdk.__all__ == ["Rest", "generate_hash"]


def test_each_declared_export_is_the_object_its_own_module_defines():
    assert oddshawk_sdk.Rest is rest_mod.Rest
    assert oddshawk_sdk.generate_hash is hashing_mod.generate_hash
