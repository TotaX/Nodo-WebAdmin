#!/bin/sh
# Modified By: Fernando F Nicola <nicolaff@gmail.com>
# To: LUGRo-Mesh

PATH=/bin:/usr/bin:/sbin:/usr/sbin
echo -e "Content-type: text/html\n\n"


NORMAL=`echo "$QUERY_STRING" | sed -n 's/^.*normal=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
LIST_BLOCKED_MAC=$(uci get "mac_list.@Macblocked[0].mac")
#LIST_BLOCKED_MAC="00:24:2b:3b:dc:c1 90:4c:e5:4a:98:e7 00:1e:8c:d5:4c:12 00:1e:8c:d5:4c:13 00:1e:8c:d5:4c:14 00:1e:8c:d5:4c:15"

TMP_DHCP=/tmp/dhcp.leases
for mac in $LIST_BLOCKED_MAC
do
HOST=$(grep $mac $TMP_DHCP | awk '{ print $4 }')
cat << P
	Host:$HOST | MAC: $mac | Status:<input type="checkbox" name="option3" value="$mac" checked onclick="loadForm('script.cgi','?mac='+this.value+'&checked='+this.checked,null)" /> [Checked=BLOCKED]<br/>
P
done

for mac in $(awk '{print $2}' $TMP_DHCP)
do
	filter="false"
	for i in $LIST_BLOCKED_MAC
	do
		if [ "$mac" = "$i" ]
		then
			filter="true"
			break	
		fi
	done
	if [ $filter = "false" ]
	then
HOST=$(grep $mac $TMP_DHCP | awk '{ print $4 }')
cat << P
	Host:$HOST | MAC:$mac | Status:<input type="checkbox" name="option3" value="$mac" onclick="loadForm('script.cgi','?mac='+this.value+'&checked='+this.checked,null)" /> [Checked=BLOCKED]<br/>
P
	fi
done
