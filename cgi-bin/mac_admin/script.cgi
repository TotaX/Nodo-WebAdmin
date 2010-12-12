#!/bin/sh
# Modified By: Fernando F Nicola <nicolaff@gmail.com>
# To: LUGRo-Mesh

PATH=/bin:/usr/bin:/sbin:/usr/sbin
#/tmp/mac_list uci config file
#config Macblocked
#        list mac '00:1e:8c:d5:4c:1e'
#        list mac '00:1e:8c:d5:4c:1e'

echo -e "Content-type: text/html\n\n"

OPTION="mac_list.@Macblocked[0].mac"
MAC=`echo "$QUERY_STRING" | sed -n 's/^.*mac=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
CHECKED=`echo "$QUERY_STRING" | sed -n 's/^.*checked=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

uci_remove_list_element () {
    local option="$1"
    local value="$2"
    local list="$(uci get $option)"
    local elem

    uci delete $option
    for elem in $list; do
        if [ "$elem" != "$value" ]
		then
           uci add_list $option=$elem
		   echo
        fi
    done
}

if [ "$CHECKED" = "true" ]
then
	iwpriv ath0 addmac $MAC
	uci add_list $OPTION="$MAC"
	uci commit
fi

if [ "$CHECKED" = "false" ]
then
	iwpriv ath0 delmac $MAC
	uci_remove_list_element $OPTION $MAC
	uci commit
fi

