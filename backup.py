#!/usr/bin/env python
# coding=utf-8
# DESCRIPTION: 按照指定时间段（2019-03-01 ~ 2019-04-01）导出数据
# created on 2019/1/5 by JW
from __future__ import generators
import MySQLdb, traceback, sys, time, logging
from datetime import datetime, timedelta

args = sys.argv
reload(sys)
sys.setdefaultencoding('utf-8')
"""
备份MySQL表
"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler('info.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def result_iter(cursor, size=1000):
    buf = cursor.fetchmany(size)
    while len(buf):
        for i in buf:
            yield i
        del buf
        logger.info("processed: " + str(size))
        buf = cursor.fetchmany(size)


def timer(start, end):
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds)

def sql_exec():
    try:
        table, start_date, end_date = args[3], args[4], args[5]
        logger.info('START BACKUP %s ...' % table)
        start = time.time()
        MYSQLDB = {'db': args[2], 'user': 'plat_test', 'passwd': 'xxxx',
           'host': args[1], 'port': 3306}
        db = MySQLdb.connect(**MYSQLDB)
        while start_date <= end_date:
            cursor = db.cursor()
            sql = "select * from %s WHERE FROM_UNIXTIME(create_time) > '%s 00:00:00' and FROM_UNIXTIME(create_time) < '%s 23:59:59'" % (
            table, start_date, start_date)
            logger.info(sql)
            row_cnt = cursor.execute(sql)
            a=[ i[0] for i in cursor.description ]
            header='    '
            with open('export.csv','w') as f:
                f.write(header.join(a))
                f.write('\n')
                for row in result_iter(cursor):
                    #a=','.join([str(x) for x in row])
                    f.write('\t'.join([str(x) for x in row]))
            start_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(1)).strftime('%Y-%m-%d')
        logger.info('END BACKUP %s ...' % table)
        logger.info('TIME USED %s.' % timer(start, time.time()))
    except:
        print traceback.format_exc()
        sys.exit(0)


if __name__ == '__main__':
    if len(args) < 6:
        print ''
        print '"""'
        print '  脚本使用说明: '
        print '  ./backup.py $host $db_name $table_name $start_date(YYYY-MM-DD) $end_date(YYYY-MM-DD)'
        print '"""'
        print ''
        sys.exit(0)
    sql_exec()
