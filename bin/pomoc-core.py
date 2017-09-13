# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import sys
import os
import time
import signal

from datetime import datetime
from datetime import timezone


server_start_time = int(round(time.time() * 1000))


def main():
    module_dir = os.path.abspath(__file__)[:(-1 * len('bin/pomoc-core.py'))]
    sys.path.append(module_dir)
    signal.signal(signal.SIGINT, _sigint_handler)

    from wsgiref import simple_server
    from pomoccore.api import api

    httpd = simple_server.make_server('127.0.0.1', 8080, api)

    print("{0} Serving Pomoc Core at 127.0.0.1:8080...".format(_get_current_datetime()))

    httpd.serve_forever()
    httpd.server_close()


def _get_current_datetime():
    return datetime.now(timezone.utc).strftime("[%Y-%m-%d %H:%M:%S %z]")


def _get_timelapse(end_time, start_time):
    milliseconds = end_time - start_time
    days, milliseconds = divmod(milliseconds, 86400000)
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    seconds, milliseconds = divmod(milliseconds, 1000)

    elapsed_time = "{0} d, {1} hr, {2} min, {3} s, {4} ms".format(days, hours, minutes, seconds, milliseconds)
    return elapsed_time


def _sigint_handler(signal, frame):
    time_lapsed = _get_timelapse(int(round(time.time() * 1000)), server_start_time)
    print("\n{0} Shutting local Pomoc Core server down...".format(_get_current_datetime()))
    print("----------------------------------------")
    print("Server ran for {0}...".format(time_lapsed))
    sys.exit(0)


if __name__ == '__main__':
    main()
