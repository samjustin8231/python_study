#encoding: utf-8

import MySQLdb
import time
from datetime import datetime, timedelta ,date
import logging
import json
import sys

db_config = {
	'host' : '127.0.0.1',
	'user' :'root',
	'passwd' : '',
	'db' : 'local'
}
file_addr = "/Users/sam/call_data.log"

# 当天接通量>=1000的各个版本的接通量
sql = """select * 
    from user;
    """
def process():
	#connect db
	db = MySQLdb.connect(**db_config)
	cursor = db.cursor()


	#invite count
	inviteCount = cursor.execute(sql) # return count
	# 打印表中的多少数据
	print "\ninvite count:" + str(inviteCount)
	printData(cursor, inviteCount)# close db

	cursor.close()
	db.close()


def printData(cursor, talkCount):
    try:
        data = cursor.fetchmany(talkCount)
        # for item in data:
        # 	print item

        jsonData = []
        # 循环读取元组数据
        # 将元组数据转换为列表类型，每个条数据元素为字典类型:[{'字段1':'字段1的值','字段2':'字段2的值',...,'字段N:字段N的值'},{第二条数据},...,{第N条数据}]
        for row in data:
            result = {}
            result['id'] = row[0]
            result['name'] = row[1]
            jsonData.append(result)

            try:
                out_log = json.dumps(result, ensure_ascii=False)
                print out_log
                fw.write(out_log)
                fw.write("\n")
            except Exception, e:
                logging.error(str(e))
                fw.close()

    except:
        print 'MySQL connect fail...'
    else:
        jsondatar = json.dumps(jsonData, ensure_ascii=False)
        return jsondatar

if __name__ == "__main__":
    if len(sys.argv) > 1:
		today = datetime.strptime(sys.argv[1], "%Y%m%d")
    else:
        today = datetime.today()
    dayOfWeek = datetime.now().weekday()
    print "今天是这周的第 " + str(dayOfWeek) + " 天"
    fw = open(file_addr, "w+")
    process()


