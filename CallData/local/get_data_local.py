# encoding: utf-8

import MySQLdb
from datetime import datetime,timedelta
import logging
import json
import sys


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoderls.default(self, obj)


db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': '',
    'db': 'test'
}
file_addr = "/Users/sam/call_data.log"

# 当天接通量>=1000的各个版本的接通量
sql_today = """select inviteStart,ringStart
    from CallLog%s
    where Date(inviteStart) = Date(%s);
    """

sql_yetoday = """select * 
    from CallLog%s
    where Date(inviteStart) = Date(%s);
    """

def process():
    # connect db
    db = MySQLdb.connect(**db_config)
    cursor = db.cursor()

    params = [curWeek,today]
    inviteCount = cursor.execute(sql_today, params)  # return count
    # 打印表中的多少数据
    print "\ninvite count:" + str(inviteCount)
    printData(cursor, inviteCount)  # close db

    print "\nyestoday:"
    params = [lastWeek, yestoday]
    inviteCount = cursor.execute(sql_today, params)  # return count
    # 打印表中的多少数据
    print "\ninvite count:" + str(inviteCount)
    printData(cursor, inviteCount)  # close db

    cursor.close()
    db.close()


def printData(cursor, talkCount):
    try:
        data = cursor.fetchmany(talkCount)
        # for item in data:
        # 	print item

        jsonData = []

        datestart = datetime.strptime('1970-01-01 08:00:00', '%Y-%m-%d %H:%M:%S')
        # 循环读取元组数据
        # 将元组数据转换为列表类型，每个条数据元素为字典类型:[{'字段1':'字段1的值','字段2':'字段2的值',...,'字段N:字段N的值'},{第二条数据},...,{第N条数据}]
        for row in data:
            result = {}
            # result['inviteStart'] = row[0]
            # result['ringStart'] = row[1]
            if row[0] == datestart:
                result["inviteNum"] = 1
            else:
                result["inviteNum"] = 0

            if row[1] == datestart:
                result["ringNum"] = 1
            else:
                result["ringNum"] = 0

            result["test"] = 1
            jsonData.append(result)

            try:
                out_log = json.dumps(result, ensure_ascii=False, cls=CJsonEncoder)
                print out_log
                fw.write(out_log)
                fw.write("\n")
            except Exception, e:
                logging.error(str(e))
                fw.close()

    except:
        print 'MySQL connect fail...'
    else:
        jsondatar = json.dumps(jsonData, ensure_ascii=False, cls=CJsonEncoder)
        return jsondatar

def getCurWeek():
	"""get cur week"""
	# curWeek = time.strftime("%W")
	curWeek = today.isocalendar()[1]
	return curWeek


if __name__ == "__main__":
    if len(sys.argv) > 1:
        today = datetime.strptime(sys.argv[1], "%Y%m%d")
    else:
        today = datetime.today()
    print "today:" + str(today)
    yestoday = today + timedelta(days=-1)
    # yestoday = datetime.strptime("2017-10-17", "%Y-%m-%d")
    print "yestoday:" + str(yestoday)

    curWeek = getCurWeek()
    lastWeek = yestoday.isocalendar()[1];
    print "lastweek:",lastWeek
    print "week:",curWeek
    dayOfWeek = datetime.now().weekday()
    print "今天是这周的第 " + str(dayOfWeek) + " 天"
    fw = open(file_addr, "w+")
    process()
