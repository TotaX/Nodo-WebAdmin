#!/bin/sh
# Modified By: Fernando F Nicola <nicolaff@gmail.com>
# To: LUGRo-Mesh

GATEWAY_CLASS="bmxd.general.gateway_class"
SHARE_RATE="nwnode.ts.share_rate"
WMODE="wireless.wifi0.hwmode"
W_PRIVATE_KEY="wireless.private.key"
NODE_TS="nwnode.ts.status"
HOSTNAME="system.@system[0].hostname"
WIFIDOG_PASSWD="wifidog.node.HTTPDPassword"
WIFIDOG_CHANGE="wifidog.node.change"

case_cambio_pass ()
{
 
password=$1

fifo_in="/tmp/empty.in"			# input fifo
fifo_out="/tmp/empty.out"		# output

# -----------------------------------------------------------------------------
cmd=passwd
#cmd="./testPass.sh"
tmp="/tmp/empty.tmp"			# tempfile to store results

empty -f -L $tmp -i $fifo_in -o $fifo_out $cmd
if [ $? -eq 0 ]; then
	if [ -w $fifo_in -a -r $fifo_out ]
	then
		empty -w -v -i $fifo_out -o $fifo_in -t 5 assword: "$password\n" > /dev/null 2>&1
		empty -w -v -i $fifo_out -o $fifo_in -t 5 Retype "$password\n" > /dev/null 2>&1
		killall empty > /dev/null 2>&1
		killall passwd > /dev/null 2>&1
		echo "Root's password changed."
	else
		echo "Error: Can't find I/O fifos!"
		exit 1
	fi
else
	echo "Error: Can't start empty in daemon mode."
	exit 1
fi
rm $fifo_in
rm $fifo_out
exit 0

}

case_root_pw ()
{
	PASSWORD="$1"
	if [ ${#PASSWORD} -gt 7 -a ${#PASSWORD} -lt 64 ]
	then
		case_cambio_pass $PASSWORD
		if [ $? -ne 0 ]
		then
			echo "Root's password didn't change."
			exit 1
		else
			echo "Root's password changed.<br>"
			exit 0
		fi
	else
		echo "Hey!, root's password too short.<br>"
		exit 1
	fi
}

case_httpd_pass_change ()
{
	HTTPPASS="$1"
	HTTPUSER="$(awk -F: '{print $2}' /etc/httpd.conf)"
	if [ ${#HTTPPASS} -gt 7 -a ${#HTTPPASS} -lt 64 ];
	then
		echo "/:$HTTPUSER:$(uhttpd -m $HTTPPASS)" > /etc/httpd.conf
		echo "WEB Password changed.<br>"
		exit 0
	else
		echo "WEB Passphrase with wrong lenght.<br>"
		exit 1
	fi
}

case_httpd_user_change ()
{
		HTTPUSER2="$1"
		if [ ${#HTTPUSER2} -gt 0 -a ${#HTTPUSER2} -lt 9 ]
		then
			echo "/:$HTTPUSER2:$(awk -F: '{print $3}' /etc/httpd.conf)" > /etc/httpd.conf
			echo "WEB user changed.<br>"
			return 0
		else
			echo "Enter user name. Requires a user name of 1 to 8 characters.<br>"
			return 1
		fi
}

wpa2_pass_change ()
{
	WPA2PASS=$1
	if [ ${#WPA2PASS} -gt 7 -a ${#WPA2PASS} -lt 64 ];
	then
		uci set $W_PRIVATE_KEY="$WPA2PASS"
		uci commit wireless
		echo "WPA2 Password changed.<br>"
		return 0
	else
		echo "WPA2 Passphrase with wrong length.<br>"
		return 1
	fi
}

wifi_mode ()
{
		MODE=$1
		uci set $WMODE="$MODE"
		uci commit wireless
		echo "Wireless Mode Changed.<br>"
}

#TRAFFIC SHARE HOW MUCH DO YOU SHARE?
ap_share () 
{
    NEWVALUE=$1
	
	if [ $NEWVALUE -eq $NEWVALUE 2> /dev/null ];#chequeo si es un numero
	then
		if [[ ! -z "$NEWVALUE" && "$NEWVALUE" -gt "0" ]];
		then
			uci set $SHARE_RATE="${NEWVALUE}"
			uci set $GATEWAY_CLASS="${NEWVALUE}"
			uci commit bmxd
			uci commit nwnode
			if [ $(uci get $NODE_TS) != "0" ];
			then 
				/usr/bin/nw_ts_1 stop
				sleep 2
				/usr/bin/nw_ts_1 start
				echo "Traffic Shaping value changed.<br>"
			else
				echo "Traffic Shaping value not changed.<br>"
			fi
		else
			echo "The new value must be greater than zero and not null.<br>"
		fi
	else
		echo "New value is not a number.<br>"
	fi
}

#TS ENABLED | DISABLED
case_ts ()
{
	STATUS=$1
	if [ $STATUS == "on" ]
	then
		if [ $(uci get $NODE_TS) == 0 ]
		then 
			uci set $NODE_TS="1"
			uci commit nwnode
			/usr/bin/nw_ts_1 start
			echo "Enabling Traffic Shapping.<br>"
		else
			uci set $NODE_TS="0"
			uci commit nwnode
			/usr/bin/nw_ts_1 stop
			echo "Disabling Traffic Shapping.<br>"
		fi
	fi
}

case_hostname ()
{ 
	NEW_HOSTNAME=$1
	uci set $HOSTNAME="$NEW_HOSTNAME"
	uci commit
	echo "Hostname changed.<br>"
}

case_wifi_dog_pass ()
{
	uci set $WIFIDOG_PASSWD="$1"
	uci set $WIFIDOG_CHANGE=1
	uci commit
	echo "WiFiDog Pass changed.<br>"
}

