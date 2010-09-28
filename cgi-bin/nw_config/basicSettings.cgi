#!/bin/sh
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
ROOT_PASSWORD=`echo "$QUERY_STRING" | sed -n 's/^.*rootPass=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

WPA2_PASSPHASE=`echo "$QUERY_STRING" | sed -n 's/^.*wpa2Pass=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

######
#WEB ADMIN ACCESS User and Password
######
WEB_ADMIN_USER=`echo "$QUERY_STRING" | sed -n 's/^.*webUser=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
WEB_ADMIN_PASS=`echo "$QUERY_STRING" | sed -n 's/^.*webPass=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

WIFIDOG_ACCESS=`echo "$QUERY_STRING" | sed -n 's/^.*wifiDog=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

HOSTNAME=`echo "$QUERY_STRING" | sed -n 's/^.*hostname=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

#Select mode [11b,11g,11bg] :
WIRELESS_MODE=`echo "$QUERY_STRING" | sed -n 's/^.*wirelesMode=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`


#####
# TS = Status [1=enabled,0=disabled] | TS = HOWMUCH [0 = All your bandwidth, !=0 = other case]
####
TRAFFIC_SHAPING_STATUS=`echo "$QUERY_STRING" | sed -n 's/^.*tsStatus=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
TRAFFIC_SHAPING_HOWMUCH=`echo "$QUERY_STRING" | sed -n 's/^.*tsHowMuch=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

if [ ! -z $ROOT_PASSWORD ]
then
	echo "llamar funcion cambiar root password"
fi

if [ ! -z $WPA2_PASSPHASE ]
then
	echo "llamar funcion cambiar wpa2 password"
fi

if [ ! -z $WEB_ADMIN_USER -o ! -z $WEB_ADMIN_PASS ]
then
	echo "llamar funcion cambiar pass o usuario"
fi

if [ ! -z $WIFIDOG_ACCESS ]
then
	echo "llamar funcion cambiar pass wifidog"
fi

if [ ! -z $HOSTNAME ]
then
	echo "llamar funcion cambiar hostname"
fi

if [ ! -z $TRAFFIC_SHAPING_STATUS -a ! -z $TRAFFIC_SHAPING_HOWMUCH ]
then
	echo "cambiar traffic shaping"
fi

# our html code
echo "<html>"
echo "<head><title>Base Settings Succefully Changed!</title></head>"
echo "<body>"
echo "$QUERY_STRING"
echo "</body>"
echo "</html>"
