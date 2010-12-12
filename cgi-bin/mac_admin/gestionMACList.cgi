#!/bin/sh
# Modified By: Fernando F Nicola <nicolaff@gmail.com>
# To: LUGRo-Mesh

PATH=/bin:/usr/bin:/sbin:/usr/sbin
echo -e "Content-type: text/html\n\n"

CLEAR=`echo "$QUERY_STRING" | sed -n 's/^.*clear=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
WHITE=`echo "$QUERY_STRING" | sed -n 's/^.*white=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`
BLACK=`echo "$QUERY_STRING" | sed -n 's/^.*black=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`


option="mac_list.@Macblocked[0].mac"

if [ "$CLEAR" = "true" ]
then
	iwpriv ath0 maccmd 3
    uci delete $option
	uci commit
fi

if [ "$WHITE" = "true" ]
then
	iwpriv ath0 maccmd 1
	uci delete $option
	uci commit
fi

if [ "$BLACK" = "true" ]
then
	iwpriv ath0 maccmd 2
fi
