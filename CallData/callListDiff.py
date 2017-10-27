#encoding: utf-8

import MySQLdb
import time
from datetime import datetime, timedelta
import logging
import json
import sys

db_config_ = {
	'host' : '121.52.250.37',
	'user' :'voip_dev_rw',
	'passwd' : 'fRgxPCTaxd0u2kcN',
	'db' : 'voip'
}
db_config = {
	'host' : 'voip-mysql01',
	'user' :'voip_dev_ro',
	'passwd' : 'Garnl3qvDPPOiYqO',
	'db' : 'voip'
}
file_addr = "/opt/scripts/inter_num_callee_warning/inter_num_callee_verbose.log"


sql1 = "select count(*) as schedule_answer from cdr_schedule_%s where calldate> date_sub(now(), interval 0.5 hour) and calldate<now() and billsec>0 and dst like '0%%'"
sql2 = "select count(*) as go_asterisk_answer from cdr_asterisk_%s where calldate> date_sub(now(), interval 0.5 hour) and calldate<now() and billsec>0 "
sql3 = "select count(*) as asterisk_anser from cdr_asterisk where calldate> date_sub(now(), interval 0.5 hour) and calldate<now() and billsec>0"

def process():
	db = MySQLdb.connect(**db_config)
	cursor = db.cursor()

	week = date.isocalendar()[1]
	cursor.execute(sql1, (week))
	schedule_answer = cursor.fetchall()
	print schedule_answer
	cursor.execute(sql2, (week))
	go_asterisk_answer = cursor.fetchall()
	print go_asterisk_answer
	cursor.execute(sql3)
	asterisk_answer = cursor.fetchall()
	print asterisk_answer
	res = schedule_answer - go_asterisk_answer - asterisk_answer

	curtime = datetime.now().strftime("%Y-%m-%d-%H:%M")
	print curtime, res

	cursor.close()
	db.close()

if __name__ == "__main__":
	if len(sys.argv) > 1:
		date = datetime.strptime(sys.argv[1], "%Y%m%d")
	else:
		date = datetime.today()

	process()



