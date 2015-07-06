cd /usr/local/hbase-1.0.1.1/
cd bin/
sudo ./start-hbase.sh 

cd /usr/local/opentsdb

sudo env COMPRESSION=NONE HBASE_HOME=/usr/local/hbase-1.0.1.1 ./src/create_table.sh

tsdtmp=${TMPDIR-'/usr/local/data'}/tsd

#sudo screen -dmS tsdb
#sudo screen -list
#sudo screen -r tsdb

nohup sudo ./build/tsdb tsd --port=4242 --staticroot=build/staticroot --cachedir=/usr/local/data --auto-metric
