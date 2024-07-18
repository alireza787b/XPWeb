# app/api/endpoints.py
from fastapi import APIRouter, HTTPException
from config.config import setup_xpc_path

# Setup the X-Plane Connect path
setup_xpc_path()

import xpc

router = APIRouter()

@router.get("/datarefs")
async def get_datarefs(datarefs: str):
    """
    Fetch values of specified datarefs.
    :param datarefs: Comma-separated list of datarefs.
    :return: JSON with dataref values.
    """
    try:
        xpc_instance = xpc.XPlaneConnect()
        datarefs_list = datarefs.split(',')
        values = xpc_instance.getDREFs(datarefs_list)
        return {dataref: value for dataref, value in zip(datarefs_list, values)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/datarefs")
async def set_datarefs(data: dict):
    """
    Set values of specified datarefs.
    :param data: Dictionary with datarefs as keys and values to set.
    :return: Success message.
    """
    try:
        xpc_instance = xpc.XPlaneConnect()
        for dataref, value in data.items():
            xpc_instance.sendDREF(dataref, value)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
