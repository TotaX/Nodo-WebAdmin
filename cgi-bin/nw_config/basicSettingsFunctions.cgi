#!/bin/sh

GATEWAY_CLASS="bmxd.general.gateway_class"
SHARE_RATE="nwnode.ts.share_rate"
WMODE="wireless.wifi0.hwmode"
W_PRIVATE_KEY="wireless.private.key"
NODE_TS="nwnode.ts.status"

function case_root_pw()
{
	PASSWORD=$1
	USUARIO=root
	if [[ "${#PASSWORD}" -gt 7 && "${#PASSWORD}" -lt 64 ]];
	then
		passwd root $PASSWORD
	else
		echo "Password No Cambiado"
	fi
}

function case_httpd_pass_change()
{
	HTTPPASS="$1"
	HTTPUSER="$(awk -F: '{print $2}' /etc/httpd.conf)"
	if [[ "${#HTTPPASS}" -gt 7 && "${#HTTPPASS}" -lt 64 ]];
	then
		echo "/:$HTTPUSER:$(httpd -m $HTTPPASS)" > /etc/httpd.conf
	else
		echo "Passphrases with length wrong. $NOCHANGED_MSG"
	fi
}

function case_httpd_user_change()
{
		echo "Enter user name. Requires a user name of 1 to 8 characters:"
		HTTPUSER2=$1
		if [[ "${#HTTPUSER2}" -gt 0 && "${#HTTPUSER2}" -lt 9 ]];
		then
			echo "/:$HTTPUSER2:$(awk -F: '{print $3}' /etc/httpd.conf)" > /etc/httpd.conf
		else
			echo "User name with length wrong. $NOCHANGED_MSG"
		fi
}


function wpa2_pass_change(){
	WPA2PASS=$1
	if [[ "${#WPA2PASS}" -gt 7 && "${#WPA2PASS}" -lt 64 ]];
	then
		uci set $W_PRIVATE_KEY="$WPA2PASS"
		uci commit wireless
	else
		echo "Passphrases with length wrong. $NOCHANGED_MSG"
	fi
}

function wifi_mode()
{
		MODE=$1
		uci set $WMODE="$MODE"
		uci commit wireless
}

#TRAFFIC SHARE HOW MUCH DO YOU SHARE?
function ap_share() 
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
			if [ $(uci_get $NODE_TS) != "0" ];
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
function case_ts()
{
	STATUS=$1
	if [ $STATUS == "on" ]
	then
		if [ $(uci_get $NODE_TS) == 0 ]
		then 
		   uci set $NODE_TS="1"
		   uci commit nwnode
		   /usr/bin/nw_ts_1 start
		fi
	else
		if [ $(uci_get $NODE_TS) != 0 ]
		then
			uci set $NODE_TS="0"
			uci commit nwnode
			/usr/bin/nw_ts_1 stop
		fi
	fi
}
