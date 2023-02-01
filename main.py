#!/usr/bin/env python3

from serial.tools import list_ports
from rd6006 import RD6006

ports = list_ports.comports()
port_path = None

for port in ports:
    if "VID:PID=1A86:7523" in port.hwid:
        port_path = port.device
        break


if port_path is None:
    print("RD60XX is not connected.")
    exit(1)
else:
    print(f"port_path:{port_path}")

rd60xx = RD6006(port_path)

print(rd60xx.status())

