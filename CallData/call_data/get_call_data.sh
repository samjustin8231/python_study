python /home/yajun.sun/scripts/call_data/get_call_data.py

/usr/local/hadoop-2.4.1/bin/hadoop fs -rm /user/yajun.sun/call_data/call_data.json
/usr/local/hadoop-2.4.1/bin/hadoop fs -put /home/yajun.sun/scripts/call_data/call_data.json /user/yajun.sun/call_data/
/usr/local/imply-1.3.0/bin/import_data /home/yajun.sun/scripts/call_data/call_data_import.json

filename="call_data.json.`date -d -1day +%Y_%m_%d`"
cp /home/yajun.sun/scripts/call_data/call_data.json /home/yajun.sun/scripts/call_data/data/${filename}