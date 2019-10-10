"""  Network forensics project."""
__author__ = "Ankit Gyawali"
__copyright__ = "Copyright (C) 2019 CMU"
__license__ = "MIT"


import ast
import os
from flask import render_template, request, jsonify, Flask
from src import discover, scan

APP = Flask(__name__, static_url_path='')
os.environ["FLASK_ENV"] = "production"
os.environ["WERKZEUG_RUN_MAIN"] = "true"

@APP.route("/")
def root():
    '''
    Returns root html file.
    '''
    return render_template('index.html')

@APP.route("/scan")
def scans():
    '''
    Returns scan UI html page.
    '''
    ports = scan.scan_ports(str(request.args.get('ipadr')))
    return render_template('scan.html', ports=ports)

@APP.route("/report_discovery", methods=["POST"])
def reports_discovery():
    '''
    Creates report on the backend.
    '''
    file_to_report = open("discovery.sherlock", "w")
    file_to_report.write(str(request.form.to_dict()['hosts']))
    file_to_report.close()
    print("Report created!")
    return ""

@APP.route("/monitor")
def monitor():
    '''
    Returns templated monitor page.
    '''
    ports = scan.scan_ports(str(request.args.get('ipadr')))
    return render_template('monitor.html', ports=ports)

@APP.route("/get_ports", methods=["POST"])
def get_ports():
    '''
    Returns available ports on given host ip address.
    '''
    print("Getting ports for monitoring..")
    return jsonify({"ports": scan.scan_ports(str(request.form.to_dict()['ipadr']))})

@APP.route("/get_reports", methods=["POST"])
def ger_reports():
    '''
    Returns available reports as JSON for inbound POST requests.
    '''
    print("Reading reports to load..")
    report_send = {}
    if os.path.isfile("scan.sherlock"):
        file_scan = open("scan.sherlock", "r")
        report_send["scan"] = {}
        for app_line in file_scan.read().splitlines():
            print(app_line.split("\t")[0])
            report_send["scan"][app_line.split("\t")[0]] = ast.literal_eval(app_line.split("\t")[1])
        file_scan.close()
    if os.path.isfile("discovery.sherlock"):
        file_discovery = open("discovery.sherlock", "r")
        report_send["discovery"] = ast.literal_eval(file_discovery.read())
        file_discovery.close()
    return jsonify(report_send)

@APP.route("/report_scan", methods=["POST"])
def report_scan():
    '''
    Cretes report scan on the backend..
    '''
    scn = open("scan.sherlock", "a+")
    writes = str(request.form.to_dict()['host']) + "\t"+ str(request.form.to_dict()['ports']) + "\n"
    scn.write(writes)
    scn.close()
    print("Report created!")
    return ""

@APP.route("/discover")
def discovery():
    '''
    Returns UI for discovery page.
    '''
    if request.args.get('port').isdigit():
        port = int(request.args.get('port'))
    else:
        port = 80
    hosts = discover.map_network(str(request.args.get('cidr')), int(request.args.get('threads')))
    ports = [scan.is_port_open(host, port) for host in hosts]
    return render_template('discover.html', hosts=hosts, port=port, maps=list(zip(hosts, ports)))

if __name__ == "__main__":
    APP.run(host='0.0.0.0')
