#!/usr/bin/env python

import sys
import socket
import re
import os.path

if len(sys.argv) != 4:
    sys.exit("""Usage: port_scan.py host start_port end_port
           where 
           host is the symbolic hostname or the IP address 
           of the machine whose ports you want to scan, 
           start_port is the starting port number and end_port is the 
           ending port number""")


verbosity = 0  # set it to 1 if you want to see the result for each port separately as the scan is taking place

dst_host = sys.argv[1]
start_port = int(sys.argv[2])
end_port = int(sys.argv[3])

open_ports = []

# Scan the ports in the specified range:
for testport in range(start_port, end_port + 1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    try:
        sock.connect((dst_host, testport))
        open_ports.append(testport)
        if verbosity:
            print(testport)
        sys.stdout.write("%s" % testport)
        sys.stdout.flush()
    except:
        if verbosity:
            print("Port closed: ", testport)
        sys.stdout.write(".")
        sys.stdout.flush()

service_ports = {}
if os.path.exists("/etc/services"):
    with open("/etc/services") as IN:
        for line in IN:
            line = line.strip()
            if line == '':
                continue
            if re.match(r'^\s*#', line):
                continue
            entries = re.split(r'\s+', line)
            service_ports[entries[1]] = ' '.join(re.split(r'\s+', line))

with open("openports.txt", 'w') as OUT:
    if not open_ports:
        print("\n\nNo open ports in the range specified\n")
    else:
        print("\n\nThe open ports:\n\n")
        for k in range(0, len(open_ports)):
            if len(service_ports) > 0:
                for portname in sorted(service_ports):
                    pattern = r'^' + str(open_ports[k]) + r'/'
                    if re.search(pattern, str(portname)):
                        print("%d: %s" % (open_ports[k], service_ports[portname]))
            else:
                 print(open_ports[k])
            OUT.write("%s\n" % open_ports[k])
