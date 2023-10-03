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

if __name__== "__main__":
    app.debug = True
    app.run(host='127.0.0.1',port=5000)
    warnings.filterwarnings('ignore')
