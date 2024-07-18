# app/core/xplane_connect.py
import struct
import xpc
import logging

class XPlaneConnectWrapper:
    def __init__(self):
        self.xpc_instance = None
        self.connect_to_xplane()

    def connect_to_xplane(self):
        """
        Attempt to connect to X-Plane using X-Plane Connect.
        """
        try:
            self.xpc_instance = xpc.XPlaneConnect()
            logging.info("Connected to X-Plane successfully.")
        except Exception as e:
            logging.error(f"Failed to connect to X-Plane: {e}")
            self.xpc_instance = None

    def sendCOMM(self, comm):
        """
        Send a command to X-Plane.

        Args:
            comm (str): The command to send to X-Plane.
        
        Raises:
            ValueError: If the command is invalid.
        """
        if not comm:
            raise ValueError("comm must be non-empty.")

        buffer = struct.pack("<4sx", b"COMM")
        if len(comm) == 0 or len(comm) > 255:
            raise ValueError("comm must be a non-empty string less than 256 characters.")

        # Pack message
        fmt = "<B{0:d}s".format(len(comm))
        buffer += struct.pack(fmt, len(comm), comm.encode('utf-8'))

        # Send
        self.xpc_instance.sendUDP(buffer)
