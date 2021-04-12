import inspect
import os
import sys
import uuid
from os.path import abspath, dirname, isfile, join

import json
import requests
from requests.compat import urljoin

import settings

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


# TODO remove all the following functions (and use them in the different scenario)
def server_working():
    """Check if EnerMaps server give a response with status code 200."""
    try:
        response = requests.get(settings.ENERMAPS_SERVER)
        if not response.status_code == 200:
            raise requests.ConnectionError("EnerMaps server is not working correctly.")
        return response.ok
    except:
        raise requests.ConnectionError("EnerMaps server is not working.")


def list_layers():
    """
    Return a list of the geofile name
    but the default geofile (NUTS, LAU and default heat density map.
    """
    try:
        response = requests.get(settings.GEOFILE_ENDPOINT)
        keys = response.json().keys()
    except:
        raise requests.ConnectionError("Impossible to reach to /geofile/ endpoint.")
    geofiles = [geofile for geofile in keys if geofile not in settings.SELECTION_LAYER]
    return geofiles


def post_geofile(*filenames):
    """Post a raster on the API."""
    for filename in filenames:
        if not isinstance(filename, str):
            raise ValueError("Only string file is supported as input.")
        testdatadir = join(dirname(dirname(abspath(__file__))), "testdata")
        path = join(testdatadir, filename)
        if not isfile(path):
            raise ValueError("File doesn't exist - {}.".format(path))
        with open(path, "rb") as file:
            files = {
                "file": (
                    "frontend_name_" + str(uuid.uuid1()) + ".tif",
                    file,
                    "image/tiff",
                )
            }
            try:
                requests.post(settings.GEOFILE_ENDPOINT, files=files)
            except:
                raise requests.ConnectionError("Error occurred during the post of the file.")
    return True, len(filenames)

def list_cm():
    """ Return a list of the cm"""
    response = requests.get(settings.CM_ENDPOINT)
    try:
        cms_list = response.json()["cms"]
    except:
        raise KeyError("\"cms\" key does not exist.")
    cms = dict()
    for i, cm in enumerate(cms_list):
        try:
            pretty_name = cm["pretty_name"]
            name = cm["name"]
        except:
            raise KeyError("\"pretty_name\" key does not exist.")
        cms.update({i : [ {"name": name}, {"pretty_name": pretty_name }]})
    return cms


def create_task(cm_name: str, is_fake_cm: bool=False):
    if is_fake_cm:
        cm_name += "_fake"
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Origin': 'http://127.0.0.1:7000',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'http://127.0.0.1:7000/',
        'Accept-Language': 'fr,fr-FR;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }
    data = {"selection":
                {"type":"FeatureCollection",
                 "features":[
                     {"type":"Feature",
                      "properties":{},
                      "geometry":
                          {"type":"Polygon",
                           "coordinates":[[[-0.993347,51.407202],[-0.411072,51.41177],[-0.383606,51.012603],[-1.018982,51.036788],[-0.993347,51.407202]]]
                           }
                      }
                ]},
            "layers":["gfa_tot_curr_density.tiff"],
            "parameters":{"factor":3}}
    url = urljoin(settings.CM_ENDPOINT, cm_name + "/task")
    response = requests.post(url=url, headers=headers, json=data)
    try:
        dict_task = response.json()
        try:
            dict_task["task_id"]
        except:
            if "message" in dict_task.keys():
                raise KeyError(dict_task["message"])
            else:
                raise KeyError("Key does not exist : task_id")
    except json.JSONDecodeError as err:
        err.msg += ", content received was " + response.text
        raise err
    return response.url


def get_task(task_url: str):
    status = "PENDING"
    while status == "PENDING":
        try:
            response = requests.get(url=task_url)
        except:
            raise requests.ConnectionError("URL is not valid : {}".format(task_url))
        dict_task = response.json()
        status = dict_task["status"]
    return dict_task

def delete_task(task_url: str):
    # TODO : can delete a taks for the moment
    response = requests.delete(url=task_url, headers={'accept': 'application/json',}, allow_redirects=True)


def scenario_01():
    server_working()
    layers = list_layers()
    assert len(layers) == 0, "Layer(s) on the API : {} .".format(layers)
    post_response, layers_number = post_geofile("big_test.tif", "small_test.tif")
    assert  post_response is True, "Geofiles posting goes wrong."
    layers = list_layers()
    assert len(layers) == layers_number, "Layer(s) on the API : {} .".format(layers)
    cms = list_cm()
    assert len(cms) == 2, "CMs implemeted : {}.".format(cms)
    task_url = create_task(cm_name="BaseCM.cm_base.multiply_raster")
    get_task(task_url=task_url)
    delete_task(task_url=task_url)
    get_task(task_url=task_url)