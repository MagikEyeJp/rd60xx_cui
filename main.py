#!/usr/bin/env python3

from serial.tools import list_ports
from rd6006 import RD6006
import time

def print_info(rd60xx):
    reg = rd60xx._read_registers(0,4)
    print(f'MODEL: {reg[0]/10}\tSN: {reg[1]<<16 | reg[2]}\tFW: {reg[3]/100}')

def print_status(rd60xx):
    reg = rd60xx._read_registers(8,14)
    print(f"[SETTING] {reg[0]/rd60xx.voltres}V\t{reg[1]/rd60xx.ampres}A")
    print(f"[CURRENT] {reg[2]/rd60xx.voltres}V\t{reg[3]/rd60xx.ampres}A")
    print(f"[OUTPUT]  {'ON' if bool(reg[10]) else 'OFF'}")

def separater():
    print("--------------------------------------------------")

if __name__ == "__main__":
    ports = list_ports.comports()
    rd60xx = None
    for port in ports:
        if "VID:PID=1A86:7523" in port.hwid:
            print(f"port_path:{port.device}")
            rd60xx = RD6006(port.device)
            break

    if rd60xx is None:
        print("RD60XX not found.")
        exit(1)

    separater()
    print_info(rd60xx)
    separater()
    print_status(rd60xx)
    separater()

    while True:
        try:
            print("[o]:OUTPUT [v]:V-SET [i]:I-SET [r]:reload [q]:exit")
            key = input(">>")
            if key == "q":
                print("Exit processing...")
                rd60xx.enable = False
                exit(0)
            elif key == "r":
                separater()
                print_status(rd60xx)
                separater()
            elif key == "v" or key == "i":
                while True:
                    print("[number]:set [c]:cancel")
                    num = input(">>")
                    if num == "c":
                        separater()
                        print_status(rd60xx)
                        separater()
                        break
                    try:
                        if key == "v":
                            rd60xx.voltage = float(num)
                        else:
                            rd60xx.current = float(num)
                            separater()
                            print_status(rd60xx)
                            separater()
                        break
                    except Exception as e:
                        print("Error: Only numbers or 'c'.")
            elif key == "o":
                rd60xx.enable = False if rd60xx.enable else True
                time.sleep(0.5)
                separater()
                print_status(rd60xx)
                separater()
            elif key == "":
                separater()
                print_status(rd60xx)
                separater()
            else:
                print("Error: Only 'o','v','i','r','q'.")
                separater()
                print_status(rd60xx)
                separater()
        except BaseException:
            print("\nExit processing...")
            rd60xx.enable = False
            exit(0)
