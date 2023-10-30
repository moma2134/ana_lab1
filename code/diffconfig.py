#!/usr/bin/env python
import os
import diffios
from napalm import get_network_driver
from datetime import datetime


def compare_running_config(ip, username, password, baseline,r_name):
    driver = get_network_driver("eos")
    cisco_c7200 = driver(ip, username, password)
    try:
        print(f'Attempting Router login to {ip}')
        cisco_c7200.open()
        running_config_data = cisco_c7200.get_config()["running"]
        print(f'Login Successful. Running config Retrieved')
    except:
        print(f'Failed to get running config. Exiting Program')

    config_name = f"temp_running_config.txt"
    diff_fileanme = f'diff_config_logs.txt'

    if len(running_config_data):
        with open(file=config_name, mode="wt+", encoding="utf-8") as f:
            f.write(running_config_data.lstrip())
            print(f"Saved running config from router on IP {ip} to {config_name} file")
    else:
        print(f"No config retrieved. Unable to retrieve running config for router with IP {ip}")

    diff = diffios.Compare(baseline,config_name)
    delta = diff.delta()
    try:
        with open(file=diff_fileanme, mode="a", encoding="utf-8") as f:
            f.write(f"Config differences on current running config and {baseline} on router {r_name} at {datetime.now()}\n")
            f.write(delta)
            f.write('\n')
    except:
        print(f'Unable to store config delta in {diff_fileanme}')

def run_diff(router_login_info):
    working_directory = '/home/ana-moeez-2/lab4/default_configs/'
    #List of older saved router files
    r1_baseline_file = '/home/ana-moeez-2/lab4/default_configs/R1.txt'
    r2_baseline_file = '/home/ana-moeez-2/lab4/default_configs/R2.txt'
    r3_baseline_file = '/home/ana-moeez-2/lab4/default_configs/R3.txt'
    r4_baseline_file = '/home/ana-moeez-2/lab4/default_configs/R4.txt'
    r5_baseline_file = '/home/ana-moeez-2/lab4/default_configs/R5.txt'
    # Router Login Variables
    for ip in router_login_info:
        ip_addr = ip
        username = 'admin'
        password = 'admin'
        hostname = router_login_info[ip]

        if hostname == "R1":
            compare_running_config(ip,username,password,r1_baseline_file,hostname) 
        if hostname == "R2":
            compare_running_config(ip,username,password,r2_baseline_file,hostname)
        if hostname == "R3":
            compare_running_config(ip,username,password,r3_baseline_file,hostname)
        if hostname == "R4":
            compare_running_config(ip,username,password,r4_baseline_file,hostname)
        if hostname == "R5":
            compare_running_config(ip,username,password,r5_baseline_file,hostname)
