# -*- coding: utf-8 -*-
"""Activation tests for contain.

These tests assume the project is a (direct) subdirectory of the user's HOME.
"""
import os
from pathlib import Path
import pytest
from unittest import mock

from ....cli.activate import activate as actfun
from ....cli import activate
from ....config import config


import pytest

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

def itest_pave_project(ensureconfig_mockcli, tmpdir):
    mock_home = os.path.join(tmpdir, "test_user_home")
    mock_proj_root = os.path.join(tmpdir, "test_project_root")
    mock_shell = "/bin/bash"
    with mock.patch('containment.cli.activate.CommandLineInterface',
                    new=ensureconfig_mockcli) as CLIO,\
         mock.patch('containment.config._PROJECT_ROOT',
                    new=mock_proj_root) as mprojroot,\
         mock.patch('containment.config._HOME',
                    new=mock_home) as mhome,\
         mock.patch('containment.config._SHELL',
                    new=mock_shell) as mshell:
        # The following line causes the code to enter pave_project.
        #CLIO().ensure_config()
        print("pass")
    
def itest_mock_class_attributes():
    cli = CommandLineInterface()
    print(cli.display_config())
