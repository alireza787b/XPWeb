# app/api/datarefs.py
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Union
from pydantic import BaseModel
from core.xplane_connect import XPlaneConnectWrapper

class DatarefResponse(Dict[str, Any]):
    dataref: Union[str, List[str]]
    value: Union[Any, List[Any]]
    status: str
    message: str = None

class SetDatarefRequest(BaseModel):
    dataref: Union[str, List[str]]
    value: Union[float, List[float]]

class SetDatarefResponse(Dict[str, Any]):
    dataref: Union[str, List[str]]
    value: Union[float, List[float]]
    status: str
    message: str = None

router = APIRouter()
xpc_wrapper = XPlaneConnectWrapper()

@router.get("/get_dataref", response_model=List[DatarefResponse])
async def get_dataref(datarefs: str):
    """
    Fetch values of specified datarefs.

    Args:
        datarefs (str): Comma-separated list of datarefs.

    Returns:
        List[DatarefResponse]: A list of DatarefResponse objects with the dataref values and statuses.

    Examples:
        **Single Dataref Request:**

        ```
        GET /get_dataref?datarefs=sim/time/zulu_time_sec

        Response:
        [
            {
                "dataref": "sim/time/zulu_time_sec",
                "value": 36000.0,
                "status": "success"
            }
        ]
        ```

        **Multiple Datarefs Request:**

        ```
        GET /get_dataref?datarefs=sim/time/zulu_time_sec,sim/flightmodel/position/latitude,sim/operation/override/override_flightcontrol

        Response:
        [
            {
                "dataref": "sim/time/zulu_time_sec",
                "value": 36000.0,
                "status": "success"
            },
            {
                "dataref": "sim/flightmodel/position/latitude",
                "value": 37.615223,
                "status": "success"
            },
            {
                "dataref": "sim/operation/override/override_flightcontrol",
                "value": 0,
                "status": "success"
            }
        ]
        ```
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

@router.post("/set_dataref", response_model=SetDatarefResponse)
async def set_dataref(request: SetDatarefRequest):
    """
    Set the value of one or multiple datarefs.

    Args:
        request (SetDatarefRequest): Dataref(s) and value(s) to set.

    Returns:
        SetDatarefResponse: The status of the dataref set operation.

    Examples:
    
    ```
        **Single Dataref Request:**
        
        POST /set_dataref
        {
            "dataref": "sim/operation/override/override_flightcontrol",
            "value": 1
        }

        Response:
        {
            "dataref": "sim/operation/override/override_flightcontrol",
            "value": 1,
            "status": "success"
        }

        **Multiple Datarefs Request:**
        
        POST /set_dataref
        {
            "dataref": ["sim/operation/override/override_flightcontrol", "sim/time/zulu_time_sec"],
            "value": [1, 36000.0]
        }

        Response:
        {
            "dataref": ["sim/operation/override/override_flightcontrol", "sim/time/zulu_time_sec"],
            "value": [1, 36000.0],
            "status": "success"
        }
    ```
    """
    if not xpc_wrapper.xpc_instance:
        xpc_wrapper.connect_to_xplane()
        if not xpc_wrapper.xpc_instance:
            raise HTTPException(status_code=500, detail="Could not connect to X-Plane.")
    
    try:
        if isinstance(request.dataref, list) and isinstance(request.value, list):
            if len(request.dataref) != len(request.value):
                raise ValueError("dataref and value lists must have the same length.")
            xpc_wrapper.xpc_instance.sendDREFs(request.dataref, request.value)
            return {"dataref": request.dataref, "value": request.value, "status": "success"}
        else:
            xpc_wrapper.xpc_instance.sendDREF(request.dataref, request.value)
            return {"dataref": request.dataref, "value": request.value, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error setting dataref: {str(e)}")
