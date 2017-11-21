#encoding: utf-8
import MySQLdb
import datetime
import time
import logging
import json
import sys

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
		# 下面的转换有bug
        # elif isinstance(obj, datetime.date):
        #     return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoderls.default(self, obj)

db_config = {
	'host' : 'voip-mysql01',
	'user' :'voip_dev_ro',
	'passwd' : 'Garnl3qvDPPOiYqO',
	'db' : 'voip'
}
jsonFile = "/home/yajun.sun/scripts/call_data/call_data.json"

# 某天的所有invite记录
# and finalBev!='5002' and finalBev!='5003'
sql_cur_day = """select ver,platform,channel,Week(inviteStart) as week,ringStart,talkStart,finalBev 
	from clientCallerVoipCallLog_%s 
	where Date(inviteStart) = %s;
	"""


def getDataFromDb():
	#connect db
	db = MySQLdb.connect(**db_config)
	cursor = db.cursor()

	####################### 获取当天数据
	# 当天invite数据
	print "\n data of the day:"
	params = [week, day]
	print "sql run start time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	inviteCallCount = cursor.execute(sql_cur_day, params) # return count
	print "sql run end time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	print "\n the count of the day:" + str(inviteCallCount)
	dataType = "invite"
	# 打印表中的多少数据
	writeDataToFile(cursor, inviteCallCount, dataType, day)# close db

	cursor.close()
	db.close()


def getCurWeek():
	"""get cur week"""
	# curWeek = time.strftime("%W")
	curWeek = day.isocalendar()[1]
	return curWeek


def writeDataToFile(cursor, talkCount, dataType, mDate):
	"将cursor打印循环打印成Json格式"
	print "write start time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	try:
		data = cursor.fetchmany(talkCount)
		# for item in data:
		# 	print item

		jsonData = []
		# 循环读取元组数据
		# 将元组数据转换为列表类型，每个条数据元素为字典类型:[{'字段1':'字段1的值','字段2':'字段2的值',...,'字段N:字段N的值'},{第二条数据},...,{第N条数据}]
		for row in data:
			result = {}
			# select ver,platform,channel,Week(talkStart) as week
			result['ver'] = row[0]
			result['platform'] = row[1]
			result['channel'] = row[2]
			result["week"] = row[3]
			result['num'] = 1
			result["date"] = str(mDate)
			result["dataType"] = dataType
			result["ringStart"] = str(row[4])
			result["talkStart"] = str(row[5])
			result["finalBev"] = row[6]

			# default value = "1970-01-01 08:00:00",if failed
			if str(row[4]) != "1970-01-01 08:00:00":
				result['ringNum'] = 1
			else:
				result['ringNum'] = 0

			if str(row[5]) != "1970-01-01 08:00:00":
				result['talkNum'] = 1
			else:
				result['talkNum'] = 0

			jsonData.append(result)

			try:
				out_log = json.dumps(result, ensure_ascii=False,cls=CJsonEncoder)
				# print out_log
				fw.write(out_log)
				fw.write("\n")
			except Exception, e:
				logging.error(str(e))
				fw.close()
	except:
		print 'MySQL connect fail...'
		fw.close()
		logging.error(str(e))
	else:
		# jsondatar = json.dumps(jsonData, ensure_ascii=False,cls=CJsonEncoder)
		# return jsondatar
		print "write end time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		pass

if __name__ == "__main__":
	if len(sys.argv) > 1:
		# set the date
		day = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
	else:
		# default get yestaday data
		day = datetime.datetime.now().date()
		day = day + datetime.timedelta(days=-1)
	# yestoday = day + datetime.timedelta(days=-1)

	# get cur week
	week = getCurWeek()
	print "***********每次查询的是前一天的数据：********"
	print "date:", str(day)
	print "week:" + str(week)

	print "......正在查询数据......"
	fw = open(jsonFile, "w+")
	getDataFromDb()
	fw.close()
	print "......查询完成......"





