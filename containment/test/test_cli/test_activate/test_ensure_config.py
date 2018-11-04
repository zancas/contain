# -*- coding: utf-8 -*-
"""ensure_config tests

These tests assume the project is a (direct) subdirectory of the user's HOME.
"""
import pytest
from unittest import mock

from ....builder import CommandLineInterface


@pytest.fixture
def ensureconfig_mockcli():
    for stub in ("write_dockerfile", "build", "run"):
        setattr(CommandLineInterface, stub, mock.MagicMock(name=stub))
    return CommandLineInterface()


def test_pave_project(ensureconfig_mockcli):
    with mock.patch(
            'containment.config._Config.directory') as mconfdir,\
        mock.patch(
            'containment.config._ProjectConfig.directory') as mprojdir,\
        mock.patch(
            'containment.config._PersonalConfig.directory') as mpersdir,\
        mock.patch(
            'containment.config._ProjectCustomization.directory') as mpcdir:
        ensureconfig_mockcli.display_config()    
