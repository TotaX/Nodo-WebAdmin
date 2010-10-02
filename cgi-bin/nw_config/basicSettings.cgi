#!/bin/sh

# Modified By: Fernando F Nicola <nicolaff@gmail.com>
# To: Lugro-Mesh

. ./basicSettingsFunctions.cgi

#{
# **************** Basic Config *****************
# ***********************************************
# a. Change Root password
# b. Change WPA2 passphrase
# c. Change Web admin access
#	c.Usuario
#	c.password
# d. Change WiFiDog access
# e. Change Host Name
# f. Change Wireless mode
# g. Change Traffic Shaping Configuration
#	g.enabled
#	g.howmuch
#
#}
echo "Content-type: text/html\n"

# read in our parameters
WEB_ROOT_PASSWORD=`echo "$QUERY_STRING" | sed -n 's/^.*rootPass=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

WEB_WPA2_PASSPHASE=`echo "$QUERY_STRING" | sed -n 's/^.*wpa2Pass=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

######
#WEB ADMIN ACCESS User and Password
######
WEB_WEB_ADMIN_USER=`echo "$QUERY_STRING" | sed -n 's/^.*webUser=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
WEB_WEB_ADMIN_PASS=`echo "$QUERY_STRING" | sed -n 's/^.*webPass=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

WEB_WIFIDOG_ACCESS=`echo "$QUERY_STRING" | sed -n 's/^.*wifiDog=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

WEB_HOSTNAME=`echo "$QUERY_STRING" | sed -n 's/^.*hostname=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

#Select mode [11b,11g,11bg] :
WEB_WIRELESS_MODE=`echo "$QUERY_STRING" | sed -n 's/^.*wirelesMode=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`


#####
# TS = Status [1=enabled,0=disabled] | TS = HOWMUCH [0 = All your bandwidth, !=0 = other case]
####
WEB_TRAFFIC_SHAPING_STATUS=`echo "$QUERY_STRING" | sed -n 's/^.*tsStatus=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
WEB_TRAFFIC_SHAPING_HOWMUCH=`echo "$QUERY_STRING" | sed -n 's/^.*tsHowMuch=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`


#ACUMULADOR DE HORRORES
ACCUM=""

if [ ! -z $WEB_ROOT_PASSWORD ]
then
	case_root_pw $WEB_ROOT_PASSWORD
	if [ $? -ne 0 ]
	then 
		ACCUM=$ACCUM"<br>""ERROR: ROOT_PASSWORD<br>"
	else
		ACCUM=$ACCUM"<br>""OK: ROOT_PASSWORD"
	fi
fi

if [ ! -z $WEB_WPA2_PASSPHASE ]
then
	wpa2_pass_change $WEB_WPA2_PASSPHASE
	if [ $? -ne 0 ]
	then 
		ACCUM=$ACCUM"<br>" "ERROR: WPA2_PASSPHASE<br>"
	else
		ACCUM=$ACCUM"<br>" "OK: WPA2_PASSPHASE"
	fi
fi

if [ ! -z $WEB_WEB_ADMIN_USER ]
then
	case_httpd_user_change $WEB_WEB_ADMIN_USER
	if [ $? -ne 0 ]
	then 
		ACCUM=$ACCUM"<br>" "ERROR: WEB_ADMIN_USER<br>"
	else
		ACCUM=$ACCUM"<br>" "OK: WEB_ADMIN_USER"
		HTTP_REINICIAR=1
	fi
fi

if [ ! -z $WEB_WEB_ADMIN_PASS ]
then
	case_httpd_pass_change $WEB_WEB_ADMIN_PASS
	if [ $? -ne 0 ]
	then 
		ACCUM=$ACCUM"<br>" "ERROR: WEB_ADMIN_PASS<br>"
	else
		ACCUM=$ACCUM"<br>" "OK: WEB_ADMIN_PASS"
		HTTP_REINICIAR=1
	fi
fi

if [ ! -z $HTTP_REINICIAR ]
then
	kill -9 $(pidof httpd);/etc/init.d/httpd start;
fi

if [ ! -z $WEB_WIFIDOG_ACCESS ]
then
	case_wifi_dog_pass $WEB_WIFIDOG_ACCESS
fi

if [ ! -z $WEB_HOSTNAME ]
then
	case_hostname $WEB_HOSTNAME
fi

if [ ! -z $WEB_TRAFFIC_SHAPING_STATUS ]
then
	case_ts $WEB_TRAFFIC_SHAPING_STATUS
fi

if [ ! -z $WEB_TRAFFIC_SHAPING_HOWMUCH ]
then
	ap_share $WEB_TRAFFIC_SHAPING_HOWMUCH
fi

if [ ! -z $WEB_WIRELESS_MODE ]
then
	wifi_mode $WEB_WIRELESS_MODE
fi

# our html code
echo "<html>"
echo "<head><title>Base Settings Changed!</title></head>"
echo "<body>"
echo "$ACCUM"
echo "</body>"
echo "</html>"
