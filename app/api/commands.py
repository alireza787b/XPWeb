# app/api/commands.py
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.core.xplane_connect import XPlaneConnectWrapper

class CommandResponse(Dict[str, Any]):
    command: str
    status: str
    message: str = None

router = APIRouter()
xpc_wrapper = XPlaneConnectWrapper()

@router.post("/command", response_model=CommandResponse)
async def send_command(command: str):
    """
        Send a command to X-Plane.

        Args:
            command (str): The command to send to X-Plane.

        Returns:
            CommandResponse: The status of the command execution.

        Example:
            Request: POST /command
            {
                "command": "sim/operation/pause_toggle"
            }
            Response:
            {
                "command": "sim/operation/pause_toggle",
                "status": "success"
            }
        """
    if not xpc_wrapper.xpc_instance:
        xpc_wrapper.connect_to_xplane()
        if not xpc_wrapper.xpc_instance:
            raise HTTPException(status_code=500, detail="Could not connect to X-Plane.")

    try:
        xpc_wrapper.sendCOMM(command)
        return {"command": command, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending command: {str(e)}")
