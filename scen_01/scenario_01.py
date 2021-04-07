import inspect
import os
import requests
import sys

import settings

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 


def scenario_01():
    #TODO implement the case in which a user adds/retrieves layers and call a non existing CM
    # (following scenario 01)
    # You can call global variables like this: settings.CM_ENDPOINT
    raise NotImplementedError("Scenario 01 not implemented")

