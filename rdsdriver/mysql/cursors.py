# Copyright openbkn.ai
#
# Licensed under the OpenBKN License.
# See LICENSE-OPENBKN.txt in the project root.

"""
MySQL游标具体实现类
"""

import pymysql.cursors

MySQLDictCursor = pymysql.cursors.DictCursor
MySQLTupleCursor = pymysql.cursors.Cursor
