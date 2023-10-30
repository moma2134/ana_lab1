#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
from jinja2 import Environment, FileSystemLoader
import healthcheck
from datetime import datetime
import diffconfig
import warnings
import json
import os
import csv

app=Flask(__name__)

# Define the Grafana dashboard URL
grafana_url = "http://localhost:3000/d/b513d541-02f4-4107-9249-95ff4054b63c/arista-r1-cpu-utilization?orgId=1&from=now-30d&to=now"

# Function to read the content of a file
def read_ipam_csv(filename):
    # Initialize an empty dictionary to store the management IPs with hostnames
    management_ips = {}
    # Open the CSV file and read it
    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        for row in csv_reader:
            if row['Interface_Type'] == 'Management':
                management_ips[row['IPv4_Address']] = row['Hostname']
    return management_ips

#Main Route
@app.route('/')
def index():
    return render_template('mainpage.html',grafana_url=grafana_url)

@app.route('/diffconfig')
def diffconfigfunction():
    router_dict = read_ipam_csv('ipam.csv')
    for router in router_dict:
       diffconfig.run_diff(router)

    with open('diff_config_logs.txt','r') as f:
        return render_template('diffconfig.html', output=f.read())

@app.route('/view_network_info')
def view_network_info():
    router_ip_list = read_ipam_csv('ipam.csv')
    links = []
    for ip in router_ip_list:
        filename = f"{router_ip_list[ip]}_Network_Info.txt"        
        # Check Ping connectivity via Management Network
        ping = healthcheck.checkPing(ip, router_ip_list[ip])
        # Get BGP Neighbors
        if router_ip_list[ip] == "R3" or router_ip_list[ip] == "R4" or router_ip_list[ip] == "R5":
            bgp_neighbor_data = healthcheck.getNeighborship(ip, router_ip_list[ip])
            bgp_neighbor = json.dumps(bgp_neighbor_data, indent=4)
        elif router_ip_list[ip] == "R1" or router_ip_list[ip] == "R2":
            ospf_neighbor_data = healthcheck.getOspfNeighborship(ip, router_ip_list[ip])
            ospf_neighbor = json.dumps(ospf_neighbor_data,indent=4)
        # Get Route Table
        route_table = healthcheck.getRoute(ip)

        with open(f'/home/ana-moeez-2/lab4/files/{filename}','w') as file:
            # Write Data for router to a file
            if router_ip_list[ip] == "R3" or router_ip_list[ip] == "R4" or router_ip_list[ip] == "R5":
                file.write(f'{ping} \n Route Table for {router_ip_list[ip]}:\n {route_table}\n BGP Neighbors for {router_ip_list[ip]}: \n {bgp_neighbor}')
            elif router_ip_list[ip] == "R1" or router_ip_list[ip] == "R2":
                file.write(f'{ping} \n Route Table for {router_ip_list[ip]}:\n {route_table}\n OSPF Neighbors for {router_ip_list[ip]}: \n {ospf_neighbor}')
            # Save filename with appropriate URL
            links.append({'filename': filename, 'url': f"/files/{filename}"})
    return render_template('view_network_info.html', links=links)

# Website Route to view Saved Router Network Health File
@app.route('/files/<filename>')
def show_file_content(filename):
    file_path = os.path.join(app.root_path, 'files', filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        return render_template('file_content.html', content=content)
    else:
        return f"The file {filename} does not exist."

# Webpage to prompt user if they want to add a config
@app.route('/add_router_config', methods=['POST'])
def router_config():
    user_response = request.form.get('user_response')
    if user_response == 'yes':
        return render_template('add_router_config.html')
    else:
        return "No new router configuration added."

# Webpage to ask type of Router Config to add
@app.route('/config_type', methods=['GET','POST'])
def config_type():
    if request.method == "POST":
        routes = {
            'OSPF': 'configure_ospf',
            'BGP': 'configure_bgp',
            'RIP': 'configure_rip',
        }
        user_configtype = request.form.get('router_config_type')
        print(user_configtype)
        # Define the routes for each router configuration type
        if user_configtype in routes:
            return redirect(url_for(routes[user_configtype]))
        return render_template('config_type.html')

#Webpage to Handle OSPF Config Input
@app.route('/configure_ospf', methods=['GET','POST'])
def configure_ospf():
    if request.method == "POST":
        ospf_id = request.form.get('ospf_id')
        ospf_router_id = request.form.get('ospf_router_id')
        ospf_networks = request.form.get('ospf_networks')
        ospf_area = request.form.get('ospf_area')
    
        template_data = {
            'ospf_id ': ospf_id,
            'ospf_router_id': ospf_router_id,
            'ospf_networks': ospf_networks,
            'ospf_area': ospf_area
        }
        print(template_data)
                # Load the Jinja2 template from a file
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('ospf.j2')  # Replace 'your_template.j2' with your template file path
        # Render the template with the data
        rendered_config = template.render(template_data)
        # Print or save the rendered configuration
        # Print or save the rendered configuration
        with open('new_router_config.txt', 'w') as file:
            file.write(rendered_config)
        return(rendered_config)
    return render_template('ospf_config.html')

# Webpage to add router config
@app.route('/show_ospf', methods=['GET'])
def show_config():
    return render_template('ospf_template', output='ospf.j2')

if __name__== "__main__":
    app.debug = True
    app.run(host='127.0.0.1',port=5000)
    warnings.filterwarnings('ignore')