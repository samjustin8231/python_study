//数据样式
select * from clientCallerVoipCallLog_43 where Date(inviteStart) = '2017-10-27' and Date(talkStart) !='1970-01-01' limit 0,1 \G;

//数据校验
select count(*)
from clientCallerVoipCallLog_43
where Date(inviteStart) = '2017-10-27';

//
select count(*) from clientCallerVoipCallLog_43 where Date(inviteStart) = '2017-10-27' and Date(ringStart) !='1970-01-01';


// 当天inviteStart所有的记录
select call_id,inviteStart,ringStart,talkStart,finishTime,ver,channel,Week(talkStart) as week,callType,isAnswered
from clientCallerVoipCallLog_43
where Date(inviteStart) = '2017-10-26' limit 0,1;

//当天各个版本的接通量:
select ver,count(*) from clientCallerVoipCallLog_43 where to_days(talkStart) = to_days(now()) and Date(talkStart)!='1970-01-01' group by ver;

//诗静：sql
select peerside_ip, peerside_recvPackets, peerside_thoeryRecvPackets, clientside_recvPackets, clientside_thoeryRecvPackets, peerside_rtpUniqRawPkts, clientside_rtpUniqRawPkts
from postmanCallerLog_43, cdr_bsterisk_43
where call_id = apostmanid
and billsec > 0 and apostmanid != "" and bpostmanid != ""  limit 0,20;

//表结构
desc clientCallerVoipCallLog_43:
+------------------+--------------+------+-----+---------+-------+
| Field            | Type         | Null | Key | Default | Extra |
+------------------+--------------+------+-----+---------+-------+
| call_id          | varchar(80)  | NO   | PRI | NULL    |       |
| callType         | int(8)       | NO   |     | NULL    |       |
| infoFlow         | varchar(200) | YES  |     | NULL    |       |
| statusFlow       | varchar(100) | YES  |     | NULL    |       |
| channel          | varchar(20)  | YES  |     | NULL    |       |
| ver              | int(8)       | YES  |     | NULL    |       |
| imei             | varchar(18)  | YES  |     | NULL    |       |
| edgeIp           | varchar(18)  | YES  |     | NULL    |       |
| mac              | varchar(18)  | YES  |     | NULL    |       |
| networkName      | varchar(50)  | YES  |     | NULL    |       |
| networkType      | int(2)       | YES  |     | NULL    |       |
| networkSubType   | int(2)       | YES  |     | NULL    |       |
| caller           | varchar(20)  | YES  | MUL | NULL    |       |
| callee           | varchar(20)  | YES  |     | NULL    |       |
| wifiBssid        | varchar(20)  | YES  |     | NULL    |       |
| callC2X          | int(2)       | YES  |     | NULL    |       |
| isAnswered       | int(2)       | YES  |     | NULL    |       |
| finalBev         | varchar(50)  | YES  |     | NULL    |       |
| isRoaming        | int(2)       | YES  |     | NULL    |       |
| city             | varchar(50)  | YES  |     | NULL    |       |
| latitude         | varchar(20)  | YES  |     | NULL    |       |
| longitude        | varchar(20)  | YES  |     | NULL    |       |
| inviteStart      | datetime     | YES  | MUL | NULL    |       |
| talkStart        | datetime     | YES  |     | NULL    |       |
| finishTime       | datetime     | YES  |     | NULL    |       |
| lastState        | varchar(50)  | YES  |     | NULL    |       |
| platform         | varchar(5)   | YES  |     | NULL    |       |
| txTol            | bigint(20)   | YES  |     | NULL    |       |
| txDis            | bigint(20)   | YES  |     | NULL    |       |
| txDup            | bigint(20)   | YES  |     | NULL    |       |
| txLoss           | bigint(20)   | YES  |     | NULL    |       |
| txRecorder       | bigint(20)   | YES  |     | NULL    |       |
| rxTol            | bigint(20)   | YES  |     | NULL    |       |
| rxDis            | bigint(20)   | YES  |     | NULL    |       |
| rxDup            | bigint(20)   | YES  |     | NULL    |       |
| rxLoss           | bigint(20)   | YES  |     | NULL    |       |
| rxRecorder       | bigint(20)   | YES  |     | NULL    |       |
| optionsStart     | datetime     | YES  |     | NULL    |       |
| optionsFinish    | datetime     | YES  |     | NULL    |       |
| rtpSelectFinish  | datetime     | YES  |     | NULL    |       |
| poststationCands | varchar(50)  | YES  |     | NULL    |       |
| rtpSelectResult  | varchar(20)  | YES  |     | NULL    |       |
| lastErr          | bigint(20)   | YES  |     | NULL    |       |
| ringStart        | datetime     | YES  |     | NULL    |       |
| callbackincoming | varchar(50)  | YES  |     | NULL    |       |
| callbackType     | varchar(50)  | YES  |     | NULL    |       |
| sdkChannel       | varchar(20)  | YES  | MUL | NULL    |       |
| sdkVersion       | int(8)       | YES  | MUL | NULL    |       |
| codeFlow         | varchar(80)  | YES  |     | NULL    |       |
+------------------+--------------+------+-----+---------+-------+

//数据样子
mysql> select * from clientCallerVoipCallLog_43 where Date(inviteStart) = '2017-10-27' and Date(talkStart) !='1970-01-01' limit 0,1 \G;
*************************** 1. row ***************************
         call_id: -3zc19AodJvgMO30uq8Cm--M2DBj5CsU
        callType: 0
        infoFlow: |Promotion Info|Promotion Info|Switching to C2P|Switching to C2P|Session Progress|Session Progress|OK|OK|hangup|
      statusFlow: CALLING|EARLY|EARLY|EARLY|EARLY|EARLY|EARLY|CONNECTING|CONFIRMED|
         channel: 0120X0
             ver: 5702
            imei: NULL
          edgeIp: 111.47.206.66
             mac: 98:71:aa:22:a2:99
     networkName: WIFI
     networkType: -1
  networkSubType: NULL
          caller: 8615817170693
          callee: 8615918447723
       wifiBssid: 50:3a:a0:d9:6e:7a
         callC2X: 1
      isAnswered: 1
        finalBev: hangup
       isRoaming: 0
            city: 全国
        latitude: NULL
       longitude: NULL
     inviteStart: 2017-10-27 12:57:28
       talkStart: 2017-10-27 12:57:54
      finishTime: 2017-10-27 12:58:26
       lastState: talking
        platform: a
           txTol: 2316
           txDis: 0
           txDup: 0
          txLoss: 0
      txRecorder: 0
           rxTol: 2779
           rxDis: 580
           rxDup: 0
          rxLoss: 0
      rxRecorder: 0
    optionsStart: 1970-01-01 08:00:00
   optionsFinish: 1970-01-01 08:00:00
 rtpSelectFinish: 1970-01-01 08:00:00
poststationCands: NULL
 rtpSelectResult: NULL
         lastErr: NULL
       ringStart: 1970-01-01 08:00:00
callbackincoming: NULL
    callbackType: NULL
      sdkChannel:
      sdkVersion: 0
        codeFlow:
1 row in set (0.00 sec)


mysql> select call_id,inviteStart,ringStart,talkStart,finishTime,ver,channel,finalBev from clientCallerVoipCallLog_43 where Date(inviteStart) = '2017-10-27' and Date(talkStart) !='1970-01-01' limit 0,100;
+-----------------------------------------+---------------------+---------------------+---------------------+---------------------+-------+-----------------+----------------------+
| call_id                                 | inviteStart         | ringStart           | talkStart           | finishTime          | ver   | channel         | finalBev             |
+-----------------------------------------+---------------------+---------------------+---------------------+---------------------+-------+-----------------+----------------------+
| 1-XV--gEKPxi0BYeH6RdDhFBy1.P.-DR        | 2017-10-27 13:04:26 | 1970-01-01 08:00:00 | 2017-10-27 13:04:47 | 2017-10-27 13:04:53 |  5702 | 0120X0          | hangup               |
| 12063763782_12063763784_1509079142656   | 2017-10-27 12:39:02 | 2017-10-27 12:39:03 | 2017-10-27 12:39:41 | 2017-10-27 12:39:48 |  1130 | SC000000        | hangup               |
| 12106343424_917525961500_1509108413806  | 2017-10-27 20:46:53 | 2017-10-27 20:46:55 | 2017-10-27 20:47:04 | 2017-10-27 20:49:18 | 55456 | OEM ASI U01 100 | Normal call clearing |
| 12134167474_971567489339_1509033862924  | 2017-10-27 00:04:22 | 2017-10-27 00:04:24 | 2017-10-27 00:04:33 | 2017-10-27 00:07:33 | 55400 | OEM ASI U01 100 | 0                    |
| 1233mY6helc7O6VngZ5l1NFICH90SExn        | 2017-10-27 23:46:17 | 1970-01-01 08:00:00 | 2017-10-27 23:46:33 | 2017-10-27 23:47:09 |  5702 | 01A050          | Normal call clearing |
| 13188203853_13184580676_1509068497934   | 2017-10-27 09:41:37 | 2017-10-27 09:41:39 | 2017-10-27 09:41:54 | 2017-10-27 09:42:10 |  1130 | SC000000        | hangup               |
| 13479193715_923409518511_1509080624429  | 2017-10-27 13:03:43 | 2017-10-27 13:03:46 | 2017-10-27 13:03:58 | 2017-10-27 13:05:59 | 55456 | OEM ASI U01 100 | Normal call clearing |
| 14156586181_966553347763_1509085589747  | 2017-10-27 14:26:29 | 2017-10-27 14:26:31 | 2017-10-27 14:27:19 | 2017-10-27 14:28:17 | 55400 | OEM ASI U01 100 | 9999                 |
| 17325275689_529545559092_1509069753844  | 2017-10-27 10:02:33 | 2017-10-27 10:02:35 | 2017-10-27 10:02:47 | 2017-10-27 10:09:10 |  1130 | SC000000        | hangup               |
| 17325341044_529545559092_1509066366736  | 2017-10-27 09:06:06 | 2017-10-27 09:06:08 | 2017-10-27 09:06:27 | 2017-10-27 09:46:29 |  1130 | SC000000        | Normal call clearing |
| 17799031241_923405434538_1509091514497  | 2017-10-27 16:05:14 | 2017-10-27 16:05:18 | 2017-10-27 16:05:25 | 2017-10-27 16:06:20 | 55400 | OEM ASI U01 100 | 9999                 |
| 18008543680_85230135060_1509096297761   | 2017-10-27 17:24:57 | 2017-10-27 17:24:58 | 2017-10-27 17:25:10 | 2017-10-27 17:25:12 |  1130 | SC000000        | hangup               |
| 18164078892_448702690548_1509101277505  | 2017-10-27 18:47:57 | 2017-10-27 18:47:59 | 2017-10-27 18:48:09 | 2017-10-27 18:51:09 |  1123 | SC000000        | Normal call clearing |
| 18644023828_18434883161_150908488225    | 2017-10-27 14:14:41 | 2017-10-27 14:14:43 | 2017-10-27 14:14:50 | 2017-10-27 14:15:03 |  1130 | SC000000        | hangup               |
| 18644023828_18435429495_1509084943797   | 2017-10-27 14:15:43 | 2017-10-27 14:15:44 | 2017-10-27 14:16:16 | 2017-10-27 14:16:31 |  1130 | SC000000        | hangup               |
| 19494593335_923232727151_1509038004617  | 2017-10-27 01:13:24 | 2017-10-27 01:13:29 | 2017-10-27 01:13:59 | 2017-10-27 01:16:09 | 55400 | OEM ASI U01 100 | 0                    |
| 19802361484_918098981845_1509104632366  | 2017-10-27 19:43:52 | 2017-10-27 19:43:53 | 2017-10-27 19:44:09 | 2017-10-27 19:48:09 | 55400 | OEM ASI U01 100 | 0                    |
| 1GPyjyW4ot4EO-yrgxleetM8DlNyLBIT        | 2017-10-27 20:14:42 | 1970-01-01 08:00:00 | 2017-10-27 20:15:22 | 2017-10-27 20:27:37 |  5702 | 0120X0          | hangup               |
| 1H0o0t0RRGzGR7hcoeTP80PDiMQcbs4C        | 2017-10-27 12:22:47 | 1970-01-01 08:00:00 | 2017-10-27 12:23:02 | 2017-10-27 12:23:32 |  5702 | 01A040          | No RTP Timeout!      |
| 1q82eEDHMGm4Mg8y2eOxbw1Vxc7Y38Vw        | 2017-10-27 17:16:40 | 1970-01-01 08:00:00 | 2017-10-27 17:16:58 | 2017-10-27 17:17:24 |  5702 | 0120X0          | Normal call clearing |
| 2LX2WQ7jqVm8gIVfUMyyVsw3pRUTQuQb        | 2017-10-27 14:56:06 | 1970-01-01 08:00:00 | 2017-10-27 14:56:18 | 2017-10-27 14:56:28 |  5702 | 0120D1          | No RTP Timeout!      |
| 2qRGb1Pt3hDX2Zl0STybGD9R2B0zg5EO        | 2017-10-27 07:00:31 | 1970-01-01 08:00:00 | 2017-10-27 07:00:50 | 2017-10-27 07:02:57 |  5702 | 0120X0          | Normal call clearing |
| 2XPXBxT0XD8n-NdDq.tvUrXqY9YWZ9UB        | 2017-10-27 10:50:28 | 1970-01-01 08:00:00 | 2017-10-27 10:50:43 | 2017-10-27 10:52:34 |  5702 | 0120X0          | hangup               |
+-----------------------------------------+---------------------+---------------------+---------------------+---------------------+-------+-----------------+----------------------+
100 rows in set (0.00 sec)

mysql> select call_id,inviteStart,ringStart,talkStart,finishTime,ver,channel,finalBev from clientCallerVoipCallLog_43 where call_id = '12063763782_12063763784_1509079142656';
+---------------------------------------+---------------------+---------------------+---------------------+---------------------+------+----------+----------+
| call_id                               | inviteStart         | ringStart           | talkStart           | finishTime          | ver  | channel  | finalBev |
+---------------------------------------+---------------------+---------------------+---------------------+---------------------+------+----------+----------+
| 12063763782_12063763784_1509079142656 | 2017-10-27 12:39:02 | 2017-10-27 12:39:03 | 2017-10-27 12:39:41 | 2017-10-27 12:39:48 | 1130 | SC000000 | hangup   |
+---------------------------------------+---------------------+---------------------+---------------------+---------------------+------+----------+----------+