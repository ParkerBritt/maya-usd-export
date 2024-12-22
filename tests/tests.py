import pytest
# from maya_usd_export import interface
import maya_usd_export

import maya.standalone 
maya.standalone.initialize()



def test_foo():
    assert True == True

def pytest_sessionfinish(session, exitstatus):
    maya.standalone.uninitialize()
