#!/usr/bin/env python3
import subprocess
from napalm import get_network_driver
from loguru import logger
from tabulate import tabulate
import pyeapi
import paramiko

# Function to check if IP Connectivity is present
def checkPing(ip, host):
    # Redirect 1 ping count output to devnull
    resp = subprocess.call(["ping", "-c", "1", ip], stdout=subprocess.DEVNULL)
    if resp == 0:
        return(f"Ping of {host} was successful")
    else:
        return(f"Ping of {host} failed")

#Function to check CPU Usage
# - Code already exists from previous 

# Function to get Route Table
def getRoute(ip):
    # Set the hostname, username, and password for the device
    hostname = ip
    username = 'admin'
    password = 'admin'

    # Establish an SSH connection
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname, username=username, password=password)

    # Send the command and receive the output
    command = "show ip route"  # or "show ipv6 route" for IPv6
    stdin, stdout, stderr = ssh_client.exec_command(command)
    route = stdout.read().decode()
    # Close the SSH connection
    ssh_client.close()
    return route

# Get Route method using Arista's API in JSON format
'''
        # Set the connection parameters
        connection = pyeapi.client.connect(
            transport="https",
            host=ip,
            username="admin",
            password="admin",
            port="443",
        )
        # Create a node object
        node = pyeapi.client.Node(connection)
        # Send the command and receive the output
        command = "show ip route"  # or "show ipv6 route" for IPv6
        output = node.enable(command)

        print(f"Route Table for {ip_list[ip]}:")
        print(json.dumps(output, indent=4))
'''

def getOspfNeighborship(ip, host):
    # Set the hostname, username, and password for the device
    hostname = ip
    username = 'admin'
    password = 'admin'

    # Establish an SSH connection
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname, username=username, password=password)

    # Send the command and receive the output
    command = "show ip ospf neighbor"  # or "show ipv6 route" for IPv6
    stdin, stdout, stderr = ssh_client.exec_command(command)
    ospf_raw = stdout.read().decode()
    # Close the SSH connection
    ssh_client.close()

    # Format the output into a table
    ospf_lines = [line.split() for line in ospf_raw.split('\n') if line.strip()]
    headers = ospf_lines[0]
    ospf_data = ospf_lines[1:]
    formatted_output = tabulate(ospf_data, headers, tablefmt="grid")

    return formatted_output


#Function to get Neighborships Information for R3, R4, & R5
def getNeighborship(ip, host):
    # Define the device parameters
    username = 'admin'
    password = 'admin'
    driver = get_network_driver('eos')

    # Connect to each device
    device = driver(hostname=ip, username=username, password=password)
    try:
        device.open()
        # Retrieve BGP neighbors
        bgp_neighbors = device.get_bgp_neighbors()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        device.close()
    return bgp_neighbors