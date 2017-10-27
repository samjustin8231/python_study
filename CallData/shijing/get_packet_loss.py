#encoding=utf-8
import MySQLdb
import datetime
import time
import json
from postman_map import postman_node_map
import logging
import sys

# 数据库连接
db_config = {
	'host' : 'voip-mysql01',
	'user' :'voip_dev_ro',
	'passwd' : 'Garnl3qvDPPOiYqO',
	'db' : 'voip'
}
filepath = "/home/yajun.sun/scripts/packet_loss/voip_packetLoss_data.json"
logfile = "/home/yajun.sun/scripts/packet_loss/packetLoss_error.log"

db = MySQLdb.connect(**db_config)
cur = db.cursor()
fw = open(filepath, "w+")

def do_execute(sql, params, call_type, client_type):
    print "sql:%s" % sql
    print "search before time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        cur.execute(sql, params)
        res = cur.fetchall()
    except Exception, e:
        logging.error(str(e))
    print "search after time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    print "write before time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for item in res:
        data = {}
        # get ip
        ip = item[0]
        if ip in postman_node_map:
            # get regin and channel
            names = postman_node_map[ip].split("_")
            data["region"] = names[0]
            data["channel"] = names[1]

            data["date"] = str(yestoday)
            data["type"] = call_type
            data["client_type"] = client_type
            data["peerside_recvPackets"] = item[1]
            data["peerside_thoeryRecvPackets"] = item[2]             
            data["clientside_recvPackets"] = item[3]
            data["clientside_thoeryRecvPackets"] = item[4]
            data["peerside_rawRecvPackets"] = item[5]
            data["clientside_rawRecvPackets"] = item[6]
            if item[4] == 0 or item[2] == 0:
                continue
            if item[3] > item[4]:
                client_pktsloss = 0
            else:
                client_pktsloss = 1 - item[3] / float(item[4])
            if item[1] > item[2]:
                peer_pktsloss = 0
            else:
                peer_pktsloss = 1 - item[1] / float(item[2])
            if item[5] > item[2]:
                peer_rawloss = 0
            else:
                peer_rawloss = 1 - item[5] / float(item[2])
            if item[6] > item[4]:
                client_rawloss = 0
            else:
                client_rawloss = 1 - item[6] / float(item[4])
            data["clientside_pktsloss"] = round(client_pktsloss, 7)
            data["peerside_pktsloss"] = round(peer_pktsloss, 7)
            data["client_rawloss"] = round(client_rawloss, 7)
            data["peer_rawloss"] = round(peer_rawloss, 7)
            data["num"] = 1
            if client_pktsloss > 0.01:
                data["cs_bigger_1%_num"] = 1
            else:
                data["cs_bigger_1%_num"] = 0
            try:
                out_log = json.dumps(data)
                fw.write(out_log)
                fw.write("\n")
            except Exception, e:
                logging.error(str(e))
                fw.close()
    print "write after time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())   

def get_c2p_data(today, yestoday, week):
    sql = """
    select peerside_ip, peerside_recvPackets, peerside_thoeryRecvPackets, clientside_recvPackets, clientside_thoeryRecvPackets, peerside_rtpUniqRawPkts, clientside_rtpUniqRawPkts
    from postmanCallerLog_%s, cdr_asterisk_%s 
    where call_id = sipcallid
    and billsec > 0
    and calldate > %s and calldate < %s
    """
    params = [week, week, yestoday, today]
    do_execute(sql, params, "c2p", "caller")

def get_c2c_data(today, yestoday, week):
    sql = """
    select peerside_ip, peerside_recvPackets, peerside_thoeryRecvPackets, clientside_recvPackets, clientside_thoeryRecvPackets, peerside_rtpUniqRawPkts, clientside_rtpUniqRawPkts
    from postmanCallerLog_%s, C2CCallLog_%s
    where C2CCallLog_%s.Call_Id = postmanCallerLog_%s.call_id
    and Establish_time is not null 
    and Invite_time > %s and Invite_time < %s
    """
    sql1 = """
    select peerside_ip, peerside_recvPackets, peerside_thoeryRecvPackets, clientside_recvPackets, clientside_thoeryRecvPackets, peerside_rtpUniqRawPkts, clientside_rtpUniqRawPkts
    from postmanCalleeLog_%s, C2CCallLog_%s
    where postmanCalleeLog_%s.call_id = concat(C2CCallLog_%s.Call_Id, "_000")
    and Establish_time is not null 
    and Invite_time > %s and Invite_time < %s
    """
    params = [week, week, week, week, yestoday, today]
    do_execute(sql, params, "c2c", "caller")
    do_execute(sql1, params, "c2c", "callee")

def get_back_data(today, yestoday, week):
    sql = """
    select peerside_ip, peerside_recvPackets, peerside_thoeryRecvPackets, clientside_recvPackets, clientside_thoeryRecvPackets, peerside_rtpUniqRawPkts, clientside_rtpUniqRawPkts
    from postmanCallerLog_%s, cdr_bsterisk_%s
    where call_id = apostmanid
    and billsec > 0 and apostmanid != "" and bpostmanid != ""
    and acalltime > %s and acalltime < %s  limit 0,20;
    """

    sql1 = """
    select peerside_ip, peerside_recvPackets, peerside_thoeryRecvPackets, clientside_recvPackets, clientside_thoeryRecvPackets, peerside_rtpUniqRawPkts, clientside_rtpUniqRawPkts
    from postmanCalleeLog_%s, cdr_bsterisk_%s
    where call_id = bpostmanid
    and billsec > 0 and apostmanid != "" and bpostmanid != ""
    and acalltime > %s and acalltime < %s 
    """

    params = [week, week, yestoday, today]
    do_execute(sql, params, "back", "caller")
    do_execute(sql, params, "back", "callee")

if __name__ == "__main__":
    logging.basicConfig(filename=logfile,format = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s", level=logging.DEBUG)        
    if len(sys.argv) > 1:
        today = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    else:
        today = datetime.datetime.now().date()
    yestoday = today +datetime.timedelta(days=-1)
    week = yestoday.isocalendar()[1]
    print "yestoday:", str(yestoday)
    print "week:", str(week)
    print "today:", str(today)
    try:
        # get_c2p_data(today, yestoday, week)
        # get_c2c_data(today, yestoday, week)
        get_back_data(today, yestoday, week)
    except Exception, e:
        cur.close()
        db.close()
        fw.close()
        logging.error(str(e))
    
    cur.close()
    db.close()
    fw.close()






