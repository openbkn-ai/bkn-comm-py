# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

"""
KDB游标具体实现类
"""

import ksycopg2.extensions
import ksycopg2.extras

KDB9DictCursor = ksycopg2.extras.RealDictCursor
KDB9TupleCursor = ksycopg2.extensions.cursor
