"""  Monitors provided host for open ports on terminal."""
__author__ = "Ankit Gyawali"
__copyright__ = "Copyright (C) 2019 CMU"
__license__ = "MIT"

import sys
import sched
import time
import scan


def do_scan(scans, interval, first_run, bucket, trail_bucket):
    '''
    Perform an scan of given port and notify if new hosts were found.
    '''
    lst = scan.scan_silent(HOST)
    trail_bucket = bucket
    bucket = lst
    if first_run is False:
        if not bucket == trail_bucket:
            print("WARNING! Ports CHANGED.")
    if first_run is True:
        first_run = False
    print(f"Discovered ports: {str(lst)}")
    LOOP_RUN.enter(INTERVAL, 1, do_scan, (scans, interval, first_run, bucket, trail_bucket))
if __name__ == '__main__':
    INTERVAL = 5
    FIRST_RUN = True
    BUCKET = []
    TRAIL_BUCKET = []
    print("Please provide a single host to scan for open ports.")
    print("Optional thread numbers as second argument.")
    HOST = "127.0.0.1"
    if len(sys.argv) == 2:
        HOST = str(sys.argv[1])
    if len(sys.argv) == 3:
        HOST = str(sys.argv[1])
        if sys.argv[2].isdigit():
            INTERVAL = int(sys.argv[2])

    print(f"Now monitoring {HOST} for open ports every {INTERVAL} seconds.")
    print('Press: "CTRL + C" to exit.')
    LOOP_RUN = sched.scheduler(time.time, time.sleep)
    LOOP_RUN.enter(INTERVAL, 1, do_scan, (LOOP_RUN, INTERVAL, FIRST_RUN, BUCKET, TRAIL_BUCKET))
    LOOP_RUN.run()
