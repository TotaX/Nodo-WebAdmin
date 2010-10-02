#!/bin/sh
# Modified By: Fernando F Nicola <nicolaff@gmail.com>
# To: Lugro-Mesh

GATEWAY_CLASS="bmxd.general.gateway_class"
SHARE_RATE="nwnode.ts.share_rate"
WMODE="wireless.wifi0.hwmode"
W_PRIVATE_KEY="wireless.private.key"
NODE_TS="nwnode.ts.status"
HOSTNAME="system.@system[0].hostname"
WIFIDOG_PASSWD="wifidog.node.HTTPDPassword"
WIFIDOG_CHANGE="wifidog.node.change"

case_root_pw ()
{
	CMD=./changeRootPass.sh
	PASSWORD="$1"
	if [ ${#PASSWORD} -gt 7 -a ${#PASSWORD} -lt 64 ]
	then
		$CMD $PASSWORD
		if [ $? != 0 ]
		then
			echo "<p><b> Error al cambiar el password de root</b></p>"
			return 1
		else
			echo "<p><b> Password de root cambiado OK</b></p>"
			return 0
		fi
	else
		echo "<h1>Hey! Coloca otro password, solo se permite numeros y letras</h1>"
		return 1
	fi
}

case_httpd_pass_change ()
{
	HTTPPASS="$1"
	HTTPUSER="$(awk -F: '{print $2}' /etc/httpd.conf)"
	if [[ "${#HTTPPASS}" -gt 7 && "${#HTTPPASS}" -lt 64 ]];
	then
		echo "/:$HTTPUSER:$(httpd -m $HTTPPASS)" > /etc/httpd.conf
		return 0
	else
		echo "Passphrases with length wrong. $NOCHANGED_MSG"
		return 1
	fi
}

case_httpd_user_change ()
{
		echo "Enter user name. Requires a user name of 1 to 8 characters:"
		HTTPUSER2=$1
		if [ ${#HTTPUSER2} -gt 0 -a ${#HTTPUSER2} -lt 9 ]
		then
			echo "/:$HTTPUSER2:$(awk -F: '{print $3}' /etc/httpd.conf)" > /etc/httpd.conf
			return 0
		else
			echo "User name with length wrong. $NOCHANGED_MSG"
			return 1
		fi
}

wpa2_pass_change ()
{
	WPA2PASS=$1
	if [[ "${#WPA2PASS}" -gt 7 && "${#WPA2PASS}" -lt 64 ]];
	then
		uci set $W_PRIVATE_KEY="$WPA2PASS"
		uci commit wireless
		return 0
	else
		echo "Passphrases with length wrong. $NOCHANGED_MSG"
		return 1
	fi
}

wifi_mode ()
{
		MODE=$1
		uci set $WMODE="$MODE"
		uci commit wireless
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
			fi
		else
			echo "The new value must be greater than zero and not null"
		fi
	else
		echo "New value is not a number."
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
		fi
	else
		if [ $(uci get $NODE_TS) != 0 ]
		then
			uci set $NODE_TS="0"
			uci commit nwnode
			/usr/bin/nw_ts_1 stop
		fi
	fi
}

case_hostname ()
{ 
	NEW_HOSTNAME=$1
	uci set $HOSTNAME="NEW_HOSTNAME"
	uci commit
}

case_wifi_dog_pass ()
{
	uci set $WIFIDOG_PASSWD=$1
	uci set $WIFIDOG_CHANGE=1
	uci commit
}
