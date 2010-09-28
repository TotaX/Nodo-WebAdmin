BMX="bmx_mode.node.mode"
GATEWAY_CLASS="bmxd.general.gateway_class"
ROUTING_CLASS="bmxd.general.routing_class"
VIS_SRV="bmxd.general.visualisation_srv"
HOSTNAME="system.@system[0].hostname"
SERVERLOG="system.@system[0].log_ip"
CHANNEL="wireless.wifi0.channel"
WMODE="wireless.wifi0.hwmode"
AMODE="wireless.wifi0.antenna"
W_PRIVATE_KEY="wireless.private.key"
BSSID="wireless.mesh.bssid"
PUBLIC_AP_SSID="wireless.public.ssid"
PUBLIC_SSID="nwnode.public.ssid"
SHARE_RATE="nwnode.ts.share_rate"
PRIVATE_AP_SSID="wireless.private.ssid"
PRIVATE_SSID="nwnode.private.ssid"
WIFIDOG_SERVER="wifidog.node.server"
WIFIDOG_SSL="wifidog.node.ssl"
WIFIDOG_PASSWD="wifidog.node.HTTPDPassword"
WIFIDOG_CHANGE="wifidog.node.change"
NODE_ID=$(uci get wifidog.node.id)
NODE_TS="nwnode.ts.status"
RESOLV_CONF="/etc/resolv.conf.default"
VERSION="/etc/nightwing_version"

function case_root_pw()
{
			PASSWORD=$1
			USUARIO=root
			passwd root $PASSWORD
}

function case_httpd_pass_change()
{
		HTTPPASS=$1
		if [[ "${#HTTPPASS}" -gt 7 && "${#HTTPPASS}" -lt 64 ]];
		then
			echo "/:$HTTPUSER:$(httpd -m $HTTPPASS)" > /etc/httpd.conf
			HTTPD_CHANGE=1
		else
			echo "Passphrases with length wrong. $NOCHANGED_MSG"
			echo $YESNO_MSG
			case_httpd_access
		fi
}
function case_httpd_user_change()
{
		echo "Enter user name. Requires a user name of 1 to 8 characters:"
		read HTTPUSER2
		if [[ "${#HTTPUSER2}" -gt 0 && "${#HTTPUSER2}" -lt 9 ]];
		then
			echo "/:$HTTPUSER2:$(awk -F: '{print $3}' /etc/httpd.conf)" > /etc/httpd.conf
			HTTPD_CHANGE=1
		else
			echo "User name with length wrong. $NOCHANGED_MSG"
			echo $YESNO_MSG
			case_httpd_access
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
			echo $YESNO_MSG
			case_wpa2_pass
		fi
}

function wifi_mode()
{
		MODE=$1
		uci set $WMODE="$MODE"
		uci commit wireless
}


function ap_share()
{
    NEWVALUE=$1
		if [ $NEWVALUE -eq $NEWVALUE 2> /dev/null ];
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
			    sleep 2
			    echo $YESNO_MSG
	    		    case_ap_share
			fi
		else
		    echo "New value is not a number."
		    sleep 2
		    echo $YESNO_MSG
		    case_ap_share
		fi
		;;
}

case_ts_select()
{
    case_ts()
    {
    if [ $(uci_get $NODE_TS) != 0 ]
	then 
	   uci set $NODE_TS="0"
	   uci commit nwnode
	   /usr/bin/nw_ts_1 stop
	else
	   uci set $NODE_TS="1"
	   uci commit nwnode
	   /usr/bin/nw_ts_1 start
    fi
    }
read VAL
case $VAL in
		y|Y)
			case_ts
			;;
		n|N)
			echo $NOCHANGED_MSG
			sleep 2
			;;
		*)
			echo "$VAL is not a valid option"
			echo "[y/n]: "
			case_ts_select
			;;
	esac 
}
menu_ts()
{
clear
echo -e "\033[1m **************** Traffic Shapping *************\033[0m"
echo -e "\033[1m ***********************************************\033[0m"
echo -e "\033[1m a.\033[0m Enable/Disable Traffic Shapping"
echo -e "\033[1m b.\033[0m How Much Do You Want To Share"
echo -e "\033[1m c.\033[0m Back to main menu"
echo -n "Select an option [a - c]: "
read opt
case $opt in
	a|A)
		echo "Traffic Shaping is in mode: $(if [ $(uci_get $NODE_TS) != 0 ]; then echo Enable; else echo Disable;fi)"
		echo $YESNO_MSG
		case_ts_select
		menu_ts
		;;
	b|B)
		echo "The current Share Rate is:  $(uci_get $SHARE_RATE)"
		echo $YESNO_MSG
		case_ap_share
		menu_ts
		;;
	c|C)
		;;
	*)
		menu_2
		;;
esac
}
