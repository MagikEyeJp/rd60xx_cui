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
    print(f'MODEL: {reg[0]/10}\tSN: {reg[1]<<16 | reg[2]}\tFW: {reg[3]/100}')

def print_device_status(rd60xx):
    reg = rd60xx._read_registers(8,14)
    print(f"[SETTING] {reg[0]/rd60xx.voltres}V\t{reg[1]/rd60xx.ampres}A")
    print(f"[CURRENT] {reg[2]/rd60xx.voltres}V\t{reg[3]/rd60xx.ampres}A")
    print(f"[OUTPUT]  {'ON' if bool(reg[10]) else 'OFF'}\t{'CC' if bool(reg[9]) else 'CV'}")

def print_separater():
    print("----------------------------------------")

if port_path is None:
    print("RD60XX is not connected.")
    exit(1)
else:
    print(f"port_path:{port_path}")

rd60xx = RD6006(port_path)

print_separater()
print_device_info(rd60xx)
print_separater()
print_device_status(rd60xx)
print_separater()
