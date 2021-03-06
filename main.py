import requests
import uuid
from os.path import join, dirname, abspath, isfile

GEOFILE_ENDPONT ='http://127.0.0.1:7000/api/geofile/'
CM_ENDPOINT = 'http://127.0.0.1:7000/api/cm/'

def list_geofile():
    """ Return a list of the geofile name"""
    response = requests.get(GEOFILE_ENDPONT)
    print(response.json())
    geofile_name = response.json().keys()
    print(geofile_name)
    return geofile_name

def list_cm():
    """ Return a list of the cm"""
    response = requests.get(CM_ENDPOINT)
    print(response.json())
    cm_list = response.json()["cms"]
    for cm in cm_list:
        print(cm)
    return cm_list


def post_geofile(file_name):
    """ Post a raster on the API"""
    path = join(dirname(abspath(__file__)), "testdata", file_name)
    if not isfile(path):
        raise ValueError("File doesn't exist.")

    with open(path, "rb") as file:
        files = {"file": ("frontend_name_" + str(uuid.uuid1()) + ".tif", file, "image/tiff")}
        try:
            resp = requests.post(GEOFILE_ENDPONT, files=files)
            return resp.ok
        except ConnectionError:
            print("Error during the post of the file.")
            return False

if __name__ == '__main__':
    list_geofile()
    list_cm()
    post_geofile("small_test.tif")
    post_geofile("big_test.tif")