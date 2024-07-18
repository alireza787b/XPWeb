# app/api/datarefs.py
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.core.xplane_connect import XPlaneConnectWrapper

class DatarefResponse(Dict[str, Any]):
    dataref: str
    value: Any
    status: str
    message: str = None

router = APIRouter()
xpc_wrapper = XPlaneConnectWrapper()

@router.get("/datarefs", response_model=List[DatarefResponse])
async def get_datarefs(datarefs: str):
    """
        Fetch values of specified datarefs.

        Args:
            datarefs (str): Comma-separated list of datarefs.

        Returns:
            List[DatarefResponse]: A list of DatarefResponse objects with the dataref values and statuses.

        Example:
            Request: GET /datarefs?datarefs=sim/cockpit2/gauges/indicators/altitude_ft_pilot,sim/flightmodel/position/latitude
            Response: [
                {
                    "dataref": "sim/cockpit2/gauges/indicators/altitude_ft_pilot",
                    "value": 5000.0,
                    "status": "success"
                },
                {
                    "dataref": "sim/flightmodel/position/latitude",
                    "value": 37.615223,
                    "status": "success"
                }
            ]
        """
    if not xpc_wrapper.xpc_instance:
        xpc_wrapper.connect_to_xplane()
        if not xpc_wrapper.xpc_instance:
            raise HTTPException(status_code=500, detail="Could not connect to X-Plane.")

    try:
        datarefs_list = datarefs.split(',')
        values = xpc_wrapper.xpc_instance.getDREFs(datarefs_list)
        response = []
        for dataref, value in zip(datarefs_list, values):
            if value is None:
                response.append({
                    "dataref": dataref,
                    "value": None,
                    "status": "error",
                    "message": "Dataref not found"
                })
            else:
                response.append({
                    "dataref": dataref,
                    "value": value,
                    "status": "success"
                })
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching datarefs: {str(e)}")
