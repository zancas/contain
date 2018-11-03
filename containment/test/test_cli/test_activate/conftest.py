import inspect
from unittest import mock

import pytest

from ....builder import CommandLineInterface


@pytest.fixture
def ensureconfig_mockcli():
    print("ensureconfig_mockcli")
    for stub in ("write_dockerfile", "build", "run"):
        setattr(CommandLineInterface, stub, mock.MagicMock(name=stub))
    return CommandLineInterface
