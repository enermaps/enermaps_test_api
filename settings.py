def init():
    global GEOFILE_ENDPOINT
    global CM_ENDPOINT
    global ENERMAPS_SERVER
    global SELECTION_LAYER
    global NUMBER_OF_CMS
    global TASK_RESPONSE_SCHEMA

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
    NUMBER_OF_CMS = 2
    TASK_RESPONSE_SCHEMA = {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "task_id": {"type": "string"},
            "cm_name": {"type": "string"},
            "result": {"type": "object"},
        },
        "required": ["status", "task_id", "cm_name", "result"],
    }
