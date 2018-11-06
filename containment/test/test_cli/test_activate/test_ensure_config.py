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

@pytest.fixture
def mock_paths(tmpdir):
    homedir = Path(tmpdir).joinpath("USERHOME")
    persconfdir = homedir.joinpath(".containment")
    persconfdir.mkdir(parents=True)
    projdir = homedir.joinpath("PROJECT")
    projdir.mkdir()
    projconfdir = projdir.joinpath('.containment')
    persprojectsdir = persconfdir.joinpath("projects")
    persprojectsdir.mkdir(parents=True)
    persprojconfdir = persprojectsdir.joinpath("PROJECT")
    return homedir, projdir, projconfdir, persconfdir, persprojconfdir 

def test_pave_project(ensureconfig_mockcli, mock_paths):
    homedir, projdir, projconfdir, persconfdir, persprojconfdir = mock_paths
    def mexpanduser():
        return homedir
    print(mexpanduser())
    with mock.patch(
    'containment.config.os.path.expanduser', new=mexpanduser
    ) as mockexpanduser,\
    mock.patch(
    'containment.config._Config.directory', new=projdir
    ) as projdir,\
    mock.patch(
    'containment.config._ProjectConfig.directory', new=projconfdir
    ) as projconfdir,\
    mock.patch(
    'containment.config._PersonalConfig.directory', new=persconfdir
    ) as persconfdir,\
    mock.patch(
    'containment.config._ProjectCustomization.directory', new=persprojconfdir
    ) as persprojconfdir:
        persprojconfdir.mkdir()
        ensureconfig_mockcli.ensure_config()
        print(projconfdir.absolute())
        print([x for x in projconfdir.glob("*.*")])
        #assert projconfdir.joinpath("Dockerfile").exists() == True
