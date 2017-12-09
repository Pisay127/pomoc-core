# Copyright (c) 2017 Pisay127. All rights reserved.
# See the file 'LICENSE' for the full license governing this code.

import re


def get_requested_scope(scope):
    return set(re.split(', ', scope.strip().lower()))
