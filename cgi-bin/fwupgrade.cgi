#!/bin/sh
PATH=/bin:/usr/bin:/sbin:/usr/sbin

file=/tmp/$$
cat > $file
cat << EOF

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <meta HTTP-EQUIV="Content-Type" CONTENT="text/html; CHARSET=utf-8">
</head>
<body  bgcolor="#ffffff" text="#0000aa" link="#ff0000" vlink="#ff5555" alink="#aaaaff" >
<P>
EOF
skip=`sed '1{:a;s/\(name="*submitfile"*\)/\1/;t;n;ba;};/^.$/q' $file|wc -c`
# Stop all
/etc/init.d/nightwing stop 2>/dev/null
sleep 10
/etc/init.d/dropbear stop 2>/dev/null
/etc/init.d/cron stop 2>/dev/null
killall hostapd 2>/dev/null
ifconfig ath0 down
ifconfig ath1 down
ifconfig ath2 down
sleep 3
FIRMWARE="/tmp/firmware.img"
dd if=$file bs=1 skip=$((skip)) of=$FIRMWARE 2>/dev/null
sleep 3
rm -f $file >/dev/null 2>&1 
sysupgrade $FIRMWARE
reboot
cat << EOF
</body>
</html>
EOF
