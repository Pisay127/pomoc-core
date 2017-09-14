# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import sys
import os
import time
from datetime import datetime
from wsgiref import simple_server

from pomoccore.api import api


server_start_time = int(round(time.time() * 1000))


def main():
    module_dir = os.path.abspath(__file__)[:(-1 * len('bin/pomoc-core.py'))]
    sys.path.append(module_dir)

    _print_server_message('{0} Starting Pomoc Core server at 0.0.0.0:8080'.format(_get_current_datetime()), True)

    httpd = simple_server.make_server('0.0.0.0', 8080, api)

    _print_server_message('{0} Serving Pomoc Core at localhost:8080...'.format(_get_current_datetime()), True)

    httpd.serve_forever()
    httpd.server_close()


def _print_server_message(message, postmessage_line=False):
    line_string = ('-' * len(message)) + ('-' * 3)
    print(line_string)
    print(message)

    if postmessage_line:
        print(line_string)


def _get_local_time():
    return datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


def _get_current_utc_offset():
    offset = (-time.timezone // 3600) * 100
    return '{0}{1:04d}'.format('+' if offset > 0 else '-', abs(offset))


def _get_current_datetime():
    return '[{0} {1}]'.format(_get_local_time(), _get_current_utc_offset())


def _get_timelapse(end_time, start_time):
    milliseconds = end_time - start_time
    days, milliseconds = divmod(milliseconds, 86400000)
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    seconds, milliseconds = divmod(milliseconds, 1000)

    elapsed_time = '{0} d, {1} hr, {2} min, {3} s, {4} ms'.format(days, hours, minutes, seconds, milliseconds)
    return elapsed_time


def _handle_keyboard_interrupt():
    time_lapsed = _get_timelapse(int(round(time.time() * 1000)), server_start_time)
    print('')  # Note that this automatically prints a new line.
    _print_server_message('{0} Shutting local Pomoc Core server down...'.format(_get_current_datetime()))
    _print_server_message('Server ran for {0}...'.format(time_lapsed))
    sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        _handle_keyboard_interrupt()
