#!/usr/bin/env python3
from flask import Flask, render_template,request
import warnings

app=Flask(__name__)

# Define the Grafana dashboard URL
grafana_url = "http://localhost:3000/d/b513d541-02f4-4107-9249-95ff4054b63c/arista-r1-cpu-utilization?orgId=1&from=now-30d&to=now"

#Main Route
@app.route('/')
def index():
    return render_template('mainpage.html',grafana_url=grafana_url)

# Webpage to add router config
@app.route('/router_config', methods=['POST'])
def router_config():
    user_response = request.form.get('user_response')
    if user_response == 'yes':
        return render_template('add_router_config.html')
    else:
        return "No new router configuration added."
    
#Webpage to Handle OSPF Config Input
@app.route('/configure_ospf', methods=['POST'])
def configure_ospf():
    ospf_id = request.form.get('ospf_id')
    ospf_router_id = request.form.get('ospf_router_id')
    ospf_networks = request.form.getlist('ospf_networks')
    
    return render_template(
        'ospf_config.html',
        ospf_id=ospf_id,
        ospf_router_id=ospf_router_id,
        ospf_networks=ospf_networks
    )

if __name__== "__main__":
    app.debug = True
    app.run(host='127.0.0.1',port=5000)
    warnings.filterwarnings('ignore')