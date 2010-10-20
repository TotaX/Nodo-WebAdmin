#!/bin/sh
# Modified By: Fernando F Nicola <nicolaff@gmail.com>
# To: Lugro-Mesh

# read in our parameters
#WEB_ROOT_PASSWORD=`echo "$QUERY_STRING" | sed -n 's/^.*rootPass=\([^&]*\).*$/\1/p' | sed "s/%20/ /g"`

# our html code
echo -e "Content-type: text/html\n\n"
cat << HEADER
$(cat /www/cgi-bin/nw_config/header_html)
HEADER

cat << MAIN
<div id="box">
$(if [ -z $ACCUM ]; then echo "Ningun Campo Seleccionado"; else echo $ACCUM; fi)
$ACCUM
</div>
MAIN

cat << FOOTER
$(cat /www/cgi-bin/nw_config/footer_html)
FOOTER

