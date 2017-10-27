python /home/shijing.xue/scripts/packet_loss/get_packet_loss.py

/usr/local/hadoop-2.4.1/bin/hadoop fs -rm /user/shijing.xue/packet_loss/voip_packetLoss_data.json
/usr/local/hadoop-2.4.1/bin/hadoop fs -put /home/shijing.xue/scripts/packet_loss/voip_packetLoss_data.json /user/shijing.xue/packet_loss/
/usr/local/imply-1.3.0/bin/import_data /home/shijing.xue/scripts/packet_loss/voip_packetloss_import.json

filename="voip_packetLoss_data.json.`date -d -1day +%Y_%m_%d`"
cp /home/shijing.xue/scripts/packet_loss/voip_packetLoss_data.json /home/shijing.xue/scripts/packet_loss/data/${filename}