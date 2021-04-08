import inspect
import os
import sys
import uuid
from os.path import abspath, dirname, isfile, join

import requests

import settings

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


# TODO remove all the following functions (and use them in the different scenario)
def list_geofile():
    """ Return a list of the geofile name"""
    response = requests.get(settings.GEOFILE_ENDPOINT)
    print(response.json())
    geofile_name = response.json().keys()
    print(geofile_name)
    return geofile_name


def list_cm():
    """ Return a list of the cm"""
    response = requests.get(settings.CM_ENDPOINT)
    print(response.json())
    cm_list = response.json()["cms"]
    for cm in cm_list:
        print(cm)
    return cm_list


def post_geofile(file_name):
    """ Post a raster on the API"""
    paths = [
        geofile
        for geofile in os.listdir(path=join(dirname(abspath(__file__)), "testdata"))
        if geofile.endswith(".tif")
    ]

    for path in paths:
        if not isfile(path):
            raise ValueError("File doesn't exist.")

        with open(path, "rb") as file:
            files = {
                "file": (
                    "frontend_name_" + str(uuid.uuid1()) + ".tif",
                    file,
                    "image/tiff",
                )
            }
            try:
                resp = requests.post(settings.GEOFILE_ENDPOINT, files=files)
                return resp.ok
            except ConnectionError:
                print("Error during the post of the file.")
                return False


def scenario_01():
    try:
        list_geofile()
        list_cm()
        post_geofile(file_name="big_test.tif")
        post_geofile(file_name="small_test.tif")
    except:
        raise NotImplementedError("Scenario 01 not implemented")
