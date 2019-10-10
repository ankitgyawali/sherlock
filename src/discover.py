"""  Discovers availablehosts from provided cidr block."""
__author__ = "Ankit Gyawali"
__copyright__ = "Copyright (C) 2019 CMU"
__license__ = "MIT"
import os
import multiprocessing
import subprocess
import sys
from netaddr import IPNetwork

LIMIT_PARALLEL = True
LIMIT_SIZE = 512

def pinger(job_q, results_q):
    """
    Ping hosts for existence
    """
    dev_null = open(os.devnull, 'w')
    while True:
        ipaddr = job_q.get()
        if ipaddr is None:
            break
        try:
            print(f"Scanning with: timeout 2.5 ping -c1 {ipaddr}")
            subprocess.check_call(['timeout', '2.5', 'ping', '-c1', ipaddr], stdout=dev_null)
            results_q.put(ipaddr)
        # pylint: disable=W0702
        except:
            pass
def map_network(cidr, pool_size):
    """
    Check for available ips on provided cidr.
    """
    ip_list = list()
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()
    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]

    for threads in pool:
        threads.start()

    # Puts jobs on queue here
    ip_address = IPNetwork(cidr)

    if(LIMIT_PARALLEL and len(ip_address) > (LIMIT_SIZE+1)):
        ip_address = ip_address[:LIMIT_SIZE]

    for ipaddr in ip_address:
        jobs.put(str(ipaddr))

    for thread in pool:
        jobs.put(None)

    for thread in pool:
        thread.join()

    while not results.empty():
        ipresult = results.get()
        ip_list.append(ipresult)

    return ip_list

if __name__ == '__main__':
    import scan

    print("Please provide a cidr block to scan as first argument.")
    print("Optional thread numbers as second argument.")
    THREADS = 256
    CIDR = "127.0.0.1/32"
    PORT = 80
    if len(sys.argv) > 1:
        CIDR = str(sys.argv[1])
    if len(sys.argv) > 2:
        CIDR = str(sys.argv[1])
        if sys.argv[2].isdigit():
            THREADS = int(sys.argv[2])
    if len(sys.argv) > 3:
        if sys.argv[3].isdigit():
            PORT = int(sys.argv[3])
    if not "/" in CIDR:
        CIDR = CIDR + "/32"
    print(f'Now scanning "{CIDR}" for available ip with "{THREADS}" threads')
    LST_HOSTS = map_network(CIDR, THREADS)
    if LST_HOSTS:
        print("\nHosts were discovered!")
        print("\nYou can pipe the output with grep to scan for ports with scan.py.")
        print("\nHosts:\n")
        PORTS = [scan.is_port_open(host, PORT) for host in LST_HOSTS]
        for idx, host in enumerate(LST_HOSTS):
            print(f"{host}")
            print(f"\t- Port: {PORT} {'OPEN' if PORTS[idx] else 'CLOSED'}")
    else:
        print("No hosts found. Try a bigger cidr!")
