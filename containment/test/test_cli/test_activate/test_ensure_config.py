# -*- coding: utf-8 -*-
"""ensure_config tests

These tests assume the project is a (direct) subdirectory of the user's HOME.
"""
from pathlib import Path
from unittest import mock

import pytest

from ....builder import CommandLineInterface
from ....config import config


@pytest.fixture
def ensureconfig_mockcli():
    for stub in ("write_dockerfile", "build", "run"):
        setattr(CommandLineInterface, stub, mock.MagicMock(name=stub))
    return CommandLineInterface()


def test_pave_project(ensureconfig_mockcli, tmpdir):
    persconf = Path(tmpdir).joinpath("USERHOME")
    persconf.mkdir()
    projconf = persconf.joinpath("PROJECT")
    projconf.mkdir()
    projcontainconf = projconf.joinpath('.containment')
    with mock.patch(
            'containment.config._Config.directory'
        ) as mconfdir,\
        mock.patch(
            'containment.config._ProjectConfig.directory', new=projcontainconf
        ) as mprojdir,\
        mock.patch(
            'containment.config._PersonalConfig.directory'
        ) as mpersdir,\
        mock.patch(
            'containment.config._ProjectCustomization.directory'
        ) as mpcdir:
        ensureconfig_mockcli.ensure_config()
