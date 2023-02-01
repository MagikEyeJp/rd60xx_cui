#!/usr/bin/env python3

from serial.tools import list_ports
from rd6006 import RD6006

ports = list_ports.comports()
port_path = None

for port in ports:
    if "VID:PID=1A86:7523" in port.hwid:
        port_path = port.device
        break

def print_device_info(rd60xx):
    reg = rd60xx._read_registers(0,4)
    print(f'MODEL: {reg[0]/10},SN: {reg[1]<<16 | reg[2]},FW: {reg[3]/100}')

def print_device_status(rd60xx):
    reg = rd60xx._read_registers(8,14)
    print(f"OUT - V:{reg[2]/rd60xx.voltres},I:{reg[3]/rd60xx.ampres}")
    print(f"SET - V:{reg[0]/rd60xx.voltres},I:{reg[1]/rd60xx.ampres}")

if port_path is None:
    print("RD60XX is not connected.")
    exit(1)
else:
    print(f"port_path:{port_path}")

rd60xx = RD6006(port_path)

print_device_info(rd60xx)
print_device_status(rd60xx)
