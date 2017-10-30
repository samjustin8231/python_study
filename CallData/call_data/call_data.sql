//数据校验
select count(*)
from clientCallerVoipCallLog_43
where Date(inviteStart) = '2017-10-27';

select count(*) from clientCallerVoipCallLog_43 where Date(inviteStart) = '2017-10-27' and Date(ringStart) !='1970-01-01';




# 当天inviteStart所有的记录
select call_id,inviteStart,ringStart,talkStart,finishTime,ver,channel,Week(talkStart) as week,callType,isAnswered
from clientCallerVoipCallLog_43
where Date(inviteStart) = '2017-10-26' limit 0,1;