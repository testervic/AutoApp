#!/usr/bin/bash -ilex
open /Applications/NemuPlayer.app
echo "等待模拟器..."
sleep 15
declare -i i=0
declare -i j=0
SSHD=`ps -ef |grep NemuHeadless | awk '{print $11}'`
while ((i <=5))
do  
	echo "$SSHD"
	if [ "$SSHD" == "--startvm" ]  
	        then  
	            echo "检测到模拟器正在运行，执行命令！"
				adb devices
				sleep 2
				SADB=`adb devices | sed -n "2p" | awk '{print $2}'`
				#echo "$SADB"
				if [ "$SADB" == "device" ]
					then
					echo "设备连接成功$SADB"
					break
				else
					adb kill-server
					adb start-server
					RADB=`adb devices | sed -n "2p" | awk '{print $2}'`
					#echo "$SADB"
					if [ "$RADB" == "device" ]
						then
						echo "设备连接成功2$RADB"
						break
					fi
				fi
	        else
	        	echo "重新执行-$i"  
	        	sleep 2
	        	let i++
	            ps -ef |grep NemuHeadless
	fi 
done
echo "运行代码..."
python3 /Users/vic/.jenkins/workspace/GetAutoAppCode/main.py
exit 1