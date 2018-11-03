import inspect

import pytest

from ....builder import CommandLineInterface

mockattributes = ("ensure_config", "write_dockerfile", "build", "run")

def apply_operations(stop_index):
    def actual_decorator(cli_cls):
        raw_klass = cli_cls.__bases__[0]
        print(id(raw_klass))
        for stub in mockattributes[stop_index:]:
            setattr(raw_klass, stub, mock.MagicMock(name=stub))
        return raw_klass

    return actual_decorator

@pytest.fixture
def ensureconfig_mockcli():
    print("ensureconfig_mockcli")
