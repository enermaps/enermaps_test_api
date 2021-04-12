def init():
    global GEOFILE_ENDPOINT
    global CM_ENDPOINT
    global ENERMAPS_SERVER
    global SELECTION_LAYER

    GEOFILE_ENDPOINT = "http://127.0.0.1:7000/api/geofile/"
    CM_ENDPOINT = "http://127.0.0.1:7000/api/cm/"
    ENERMAPS_SERVER = "http://localhost:7000/"
    SELECTION_LAYER = [
        "lau.zip",
        "nuts0.zip",
        "nuts2.zip",
        "nuts3.zip",
        "nuts1.zip",
        "gfa_tot_curr_density.tiff",
    ]
