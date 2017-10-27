#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
import time
from datetime import datetime, timedelta
import logging
import json
import sys

db_config = {
	'host' : 'voip-mysql01',
	'user' :'voip_dev_ro',
	'passwd' : 'Garnl3qvDPPOiYqO',
	'db' : 'voip'
}
jsonFile = "call_data_json.log"

# 当周拨号量>=1000各个版本的拨号量
sql_week_ver_invite_count = """select ver,channel,count(*) as inviteCount 
	from clientCallerVoipCallLog_%s
	where to_days(inviteStart) !='1970-01-01'
	group by ver 
	having inviteCount>=1000;
	"""

# 当周响铃量>=1000各个版本的响铃量
sql_week_ver_ring_count = """select ver,channel,count(*) as ringCount 
	from clientCallerVoipCallLog_%s
	where to_days(ringStart) !='1970-01-01'
	group by ver 
	having ringCount>=1000;
	"""

# 当周接通量>=1000各个版本的接通量
sql_week_ver_talk_count = """select ver,channel,count(*) as talkCount 
	from clientCallerVoipCallLog_%s
	where to_days(talkStart) !='1970-01-01'
	group by ver 
	having talkCount>=1000;
	"""

# 当天接通量>=1000的各个版本的拨号量
sql_day_ver_invite_count = """select ver,channel,count(*) as inviteCount 
	from clientCallerVoipCallLog_%s 
	where to_days(inviteStart) = to_days(now()) 
	group by ver 
	having inviteCount>=1000;
	"""

# 当天接通量>=1000的各个版本的响铃量
sql_day_ver_ring_count = """select ver,channel,count(*) as ringCount 
	from clientCallerVoipCallLog_%s 
	where to_days(ringStart) = to_days(now()) 
	group by ver 
	having ringCount>=1000;
	"""

# 当天接通量>=1000的各个版本的接通量
sql_day_ver_talk_count = """select ver,channel,count(*) as talkCount 
	from clientCallerVoipCallLog_%s 
	where to_days(talkStart) = to_days(now()) 
	group by ver 
	having talkCount>=1000;
	"""

def process():
	#connect db
	db = MySQLdb.connect(**db_config)
	cursor = db.cursor()

	# get cur week
	curWeek = getCurWeek()

	# 当天的数据
	#invite count
	inviteCountDay = cursor.execute(sql_day_ver_invite_count,(curWeek)) # return count
	# 打印表中的多少数据
	print "\ninvite count cur day:" + str(inviteCountDay)
	fw.write("\ninvite count cur day:"+str(inviteCountDay))
	inviteJsonData = printData(cursor, inviteCountDay)# close db

	#ring count
	ringCountDay = cursor.execute(sql_day_ver_ring_count,(curWeek)) # return count
	print "\nring count cur day:" + str(ringCountDay)
	fw.write("\nring count cur day:" + str(ringCountDay))
	ringJsonData = printData(cursor, ringCountDay)# close db

	#talk count
	talkCountDay = cursor.execute(sql_day_ver_talk_count,(curWeek)) # return count
	print "\ntalk count cur day:" + str(talkCountDay)
	fw.write("\ntalk count cur day:" + str(talkCountDay))
	talkJsonData = printData(cursor, talkCountDay)# close db

	#############################
	# 当周的数据
	# invite count
	inviteCountWeek = cursor.execute(sql_week_ver_invite_count, (curWeek))  # return count
	# 打印表中的多少数据
	print "\ninvite count cur week:" + str(inviteCountWeek)
	fw.write("\ninvite count cur week:" + str(inviteCountWeek))
	fw.write("\n")
	inviteJsonData = printData(cursor, inviteCountWeek)  # close db

	# ring count
	ringCountWeek = cursor.execute(sql_week_ver_ring_count, (curWeek))  # return count
	print "\nring count cur week:" + str(ringCountWeek)
	fw.write("\nring count cur week:" + str(ringCountWeek))
	ringJsonData = printData(cursor, ringCountWeek)  # close db

	# talk count
	talkCountWeek = cursor.execute(sql_week_ver_talk_count, (curWeek))  # return count
	print "\ntalk count cur week:" + str(talkCountWeek)
	fw.write("\ntalk count cur week:" + str(talkCountWeek))
	talkJsonData = printData(cursor, talkCountWeek)  # close db

	print "\ninvite json data:\n%s" % inviteJsonData
	print "\nring json data:\n%s" % ringJsonData
	print "\ntalk json data:\n%s" % talkJsonData

	fw.write("\ninvite json data:\n%s" % inviteJsonData)
	fw.write("\nring json data:\n%s" % ringJsonData)
	fw.write("\ntalk json data:\n%s" % talkJsonData)

	# 写数据
	# fw.write(inviteJsonData)
	# f.write(ringJsonData)
	# f.write(talkJsonData)

	cursor.close()
	db.close()


def getCurWeek():
	"""get cur week"""
	# curWeek = time.strftime("%W")
	curWeek = date.isocalendar()[1]
	print "curWeek:" + str(curWeek)
	return curWeek


def printData(cursor, talkCount):
	"将cursor打印循环打印成Json格式"
	try:
		data = cursor.fetchmany(talkCount)
		# for item in data:
		# 	print item

		jsonData = []
		# 循环读取元组数据
		# 将元组数据转换为列表类型，每个条数据元素为字典类型:[{'字段1':'字段1的值','字段2':'字段2的值',...,'字段N:字段N的值'},{第二条数据},...,{第N条数据}]
		fw.write("\n")
		for row in data:
			result = {}
			result['ver'] = row[0]
			result['channel'] = row[1]
			result['count'] = row[2]
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
		fw.close()
		logging.error(str(e))
	else:
		jsondatar = json.dumps(jsonData, ensure_ascii=False)
		return jsondatar

if __name__ == "__main__":
	if len(sys.argv) > 1:
		date = datetime.strptime(sys.argv[1], "%Y%m%d")
	else:
		date = datetime.today()
	print "......正在查询数据......"
	fw = open(jsonFile, "w+")
	process()
	fw.close()
	print "......查询完成......"





