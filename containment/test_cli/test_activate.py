# -*- coding: utf-8 -*-
"""Activation tests for contain."""
import pytest
from unittest import mock

from ..builder import CommandLineInterface
from ..cli.activate import activate as actfun
from ..cli import activate



operations = ("ensure_config",
              "write_dockerfile",
              "build",
              "run")


class InitialStepFactory(type):

    def __new__(mcls, name, bases, namespace, **kwds):
        ccli = type.__new__(mcls, name, bases, namespace, **kwds)
        print("ccli is: ", ccli)
        print("Inside metaclass __new__!")
        print("mcls is: ", mcls)
        print("name is: ", name)
        print("bases are: ", bases)
        print("namespace is: ", namespace)
        print("dir(ccli): ", dir(ccli))
        print("kwds: ", kwds)
        return ccli
    

class NInitialSteps(CommandLineInterface, metaclass=InitialStepFactory):
    def __init__(self, A=1):
        print("NInitialSteps.__init__")
"""class PrimeMover(CommandLineInterface):
    def __new__(
    def __init__(self, numsteps):
        
        super(PrimeMover, self).__init__()

    def 
"""

    
def test_unitest_patch():
    print(dir(NInitialSteps()))
    print("Type expt: ")
    
    with mock.patch('containment.cli.activate.CommandLineInterface',
                    auto_spec=True) as CLIO:   
        c = CLIO()
        print(c)
        print(c.ensure_config())

@pytest.fixture
def initialoperations():
    def takesteps(number_steps):
        """"""
        newcli = CommandLineInterface()
        for ordered_op in operations[number_steps:]:
            print(ordered_op)
            newcli.__setattr__(ordered_op, mock.sentinel) 
        #print(dir(newcli))
        print(type(newcli.run))
        print(type(newcli.build))
        return newcli

    return takesteps


def test_construction(initialoperations, monkeypatch):
    """Test activation under ideal conditions."""
    with monkeypatch.context() as c:
        monkeypatch.setattr("..builder.CommandLineInterface",
                            initialoperations(3))
        actfun()


def test_ensure_config(monkeypatch):
    """Test activation under ideal conditions."""
    def initialoperations():
        newcli = CommandLineInterface()
        newcli.write_dockerfile = lambda: print("write_dockerfile")
        newcli.build = lambda: print("build")
        newcli.run = lambda: print("run")
        return newcli

    with monkeypatch.context() as m:
        m.setattr(activate, "CommandLineInterface", initialoperations)
        actfun()


def test_write_dockerfile(monkeypatch):
    """Test activation under ideal conditions."""
    def initialoperations():
        newcli = CommandLineInterface()
        newcli.build = lambda: print("build")
        newcli.run = lambda: print("run")
        return newcli

    with monkeypatch.context() as m:
        m.setattr(activate, "CommandLineInterface", initialoperations)
        actfun()


def test_build(monkeypatch):
    """Test activation under ideal conditions."""
    def initialoperations():
        newcli = CommandLineInterface()
        newcli.run = lambda: print("run")
        return newcli

    with monkeypatch.context() as m:
        m.setattr(activate, "CommandLineInterface", initialoperations)
        actfun()


def test_run(monkeypatch):
    """Test activation under ideal conditions."""
    def initialoperations():
        newcli = CommandLineInterface()
        return newcli

    with monkeypatch.context() as m:
        m.setattr(activate, "CommandLineInterface", initialoperations)
        actfun()
