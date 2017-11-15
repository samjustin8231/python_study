###################################### execute python script
#python /home/yajun.sun/scripts/call_data/get_call_data.py "2017-11-14"
python /home/yajun.sun/scripts/call_data/get_call_data.py

###################################### move data to hadoop
# delete data of hadoop
/usr/local/hadoop-2.4.1/bin/hadoop fs -rm /user/yajun.sun/call_data/call_data.json

# recopy new data
/usr/local/hadoop-2.4.1/bin/hadoop fs -put /home/yajun.sun/scripts/call_data/call_data.json /user/yajun.sun/call_data/

# import data to druid
/usr/local/imply-1.3.0/bin/import_data /home/yajun.sun/scripts/call_data/call_data_import.json

####################################### back zhe data of yesteday
# filename of yesteday
filename="call_data.json.`date -d -1day +%Y_%m_%d`"
# delete old data
rm -rf /home/yajun.sun/scripts/call_data/data/
cp /home/yajun.sun/scripts/call_data/call_data.json /home/yajun.sun/scripts/call_data/data/${filename}
