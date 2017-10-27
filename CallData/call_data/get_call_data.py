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

# 当天inviteStart所有的记录
sql_cur_day_invite = """select ver,platform,channel,Week(talkStart) as week 
   from clientCallerVoipCallLog_%s
   where Date(inviteStart) = %s;
	"""

# # 当天ringStart所有的记录
sql_cur_day_ring = """select ver,platform,channel,Week(talkStart) as week 
   from clientCallerVoipCallLog_%s
   where Date(ringStart) = %s;
	"""

# 当天talkStart所有的记录
sql_cur_day_talk = """select ver,platform,channel,Week(talkStart) as week 
   from clientCallerVoipCallLog_%s
   where Date(talkStart) = %s;
	"""
#
# # 昨天talkStart所有的记录
# sql_yestoday_talk = """select inviteStart,ringStart,talkStart,finishTime,ver,channel,Week(talkStart) as week,callType,isAnswered
#    from clientCallerVoipCallLog_%s
#    where Date(talkStart) = %s limit 0,20;
# 	"""

###############################################################################
# # 当周拨号量>=1000各个版本的拨号量
# sql_week_ver_invite_count = """select ver,channel,count(*) as inviteCount
# 	from clientCallerVoipCallLog_%s
# 	where to_days(inviteStart) !='1970-01-01';
# 	"""
#
# # 当周响铃量>=1000各个版本的响铃量
# sql_week_ver_ring_count = """select ver,channel,count(*) as ringCount
# 	from clientCallerVoipCallLog_%s
# 	where to_days(ringStart) !='1970-01-01'
# 	group by ver
# 	having ringCount>=1000 limit 0,20;
# 	"""
#
# # 当周接通量>=1000各个版本的接通量
# sql_week_ver_talk_count = """select ver,channel,count(*) as talkCount
# 	from clientCallerVoipCallLog_%s
# 	where to_days(talkStart) !='1970-01-01'
# 	group by ver
# 	having talkCount>=1000 limit 0,20;
# 	"""
#
# # 当天接通量>=1000的各个版本的拨号量
# sql_day_ver_invite_count = """select ver,channel,count(*) as inviteCount
# 	from clientCallerVoipCallLog_%s
# 	where to_days(inviteStart) = to_days(now())
# 	group by ver
# 	having inviteCount>=1000 limit 0,20;
# 	"""
#
# # 当天接通量>=1000的各个版本的响铃量
# sql_day_ver_ring_count = """select ver,channel,count(*) as ringCount
# 	from clientCallerVoipCallLog_%s
# 	where to_days(ringStart) = to_days(now())
# 	group by ver
# 	having ringCount>=1000;
# 	"""
#
# # 当天接通量>=1000的各个版本的接通量
# sql_day_ver_talk_count = """select ver,channel,count(*) as talkCount
# 	from clientCallerVoipCallLog_%s
# 	where to_days(talkStart) = to_days(now())
# 	group by ver
# 	having talkCount>=1000;
# 	"""

def process():
	#connect db
	db = MySQLdb.connect(**db_config)
	cursor = db.cursor()

	####################### 获取当天数据
	# 当天invite数据
	print "\ninvite data of cur day:"
	params = [curWeek,today]
	print "sql run start time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	inviteCallCount = cursor.execute(sql_cur_day_invite, params) # return count
	print "sql run end time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	print "\ninvite count cur day:" + str(inviteCallCount)
	dataType = "invite"
	# 打印表中的多少数据
	printData(cursor, inviteCallCount , dataType, today)# close db

	# 当天ring数据
	print "\nring data of cur day:"
	print "sql run start time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	ringCallCount = cursor.execute(sql_cur_day_ring, params)  # return count
	print "sql run end time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	print "\nring count cur day:" + str(ringCallCount)
	dataType = "ring"
	# 打印表中的多少数据
	printData(cursor, ringCallCount, dataType, today)  # close db

	# 当天talk数据
	print "\ntalk data of cur day:"
	print "sql run start time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	talkCallCount = cursor.execute(sql_cur_day_talk, params)  # return count
	print "sql run end time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	print "\ntalk count cur day:" + str(talkCallCount)
	dataType = "talk"
	# 打印表中的多少数据
	printData(cursor, ringCallCount, dataType, today)  # close db

	####################### 获取昨天数据

	# # 昨天invite数据
	# print "\ninvite data of yesteday:"
	# params = [lastWeek, yestoday]
	# inviteCallCount = cursor.execute(sql_cur_day_invite, params)  # return count
	# print "\ninvite count yesteday:" + str(inviteCallCount)
	# dataType = "invite"
	# # 打印表中的多少数据
	# printData(cursor, inviteCallCount, dataType, yestoday)  # close db
    #
    #
	# print "\nring data of yesteday:"
	# inviteCallCount = cursor.execute(sql_cur_day_ring, params)  # return count
	# print "\nring count yesteday:" + str(inviteCallCount)
	# dataType = "ring"
	# # 打印表中的多少数据
	# printData(cursor, inviteCallCount, dataType, yestoday)  # close db
    #
	# #talk count
	# print "\ntalk data of yesteday:"
	# inviteCallCount = cursor.execute(sql_cur_day_talk, params)  # return count
	# print "\ntalk count yesteday:" + str(inviteCallCount)
	# dataType = "talk"
	# # 打印表中的多少数据
	# printData(cursor, inviteCallCount, dataType, yestoday)  # close db

    #
	# #############################
	# # 当周的数据
	# # invite count
	# inviteCountWeek = cursor.execute(sql_week_ver_invite_count, (curWeek))  # return count
	# # 打印表中的多少数据
	# print "\ninvite count cur week:" + str(inviteCountWeek)
	# fw.write("\ninvite count cur week:" + str(inviteCountWeek))
	# fw.write("\n")
	# inviteJsonData = printData(cursor, inviteCountWeek)  # close db
    #
	# # ring count
	# ringCountWeek = cursor.execute(sql_week_ver_ring_count, (curWeek))  # return count
	# print "\nring count cur week:" + str(ringCountWeek)
	# fw.write("\nring count cur week:" + str(ringCountWeek))
	# ringJsonData = printData(cursor, ringCountWeek)  # close db
    #
	# # talk count
	# talkCountWeek = cursor.execute(sql_week_ver_talk_count, (curWeek))  # return count
	# print "\ntalk count cur week:" + str(talkCountWeek)
	# fw.write("\ntalk count cur week:" + str(talkCountWeek))
	# talkJsonData = printData(cursor, talkCountWeek)  # close db
    #
	# print "\ninvite json data:\n%s" % inviteJsonData
	# print "\nring json data:\n%s" % ringJsonData
	# print "\ntalk json data:\n%s" % talkJsonData
    #
	# fw.write("\ninvite json data:\n%s" % inviteJsonData)
	# fw.write("\nring json data:\n%s" % ringJsonData)
	# fw.write("\ntalk json data:\n%s" % talkJsonData)

	# 写数据
	# fw.write(inviteJsonData)
	# f.write(ringJsonData)
	# f.write(talkJsonData)

	cursor.close()
	db.close()


def getCurWeek():
	"""get cur week"""
	# curWeek = time.strftime("%W")
	curWeek = today.isocalendar()[1]
	return curWeek


def printData(cursor, talkCount, dataType ,mDate):
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
		today = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
	else:
		today = datetime.datetime.now().date()
	yestoday = today + datetime.timedelta(days=-1)

	# get cur week
	curWeek = getCurWeek()
	lastWeek = yestoday.isocalendar()[1];
	print "yestoday:", str(yestoday)
	print "today:", str(today)
	print "curWeek:" + str(curWeek)
	print "lastWeek:" + str(lastWeek)

	print "......正在查询数据......"
	fw = open(jsonFile, "w+")
	process()
	fw.close()
	print "......查询完成......"





