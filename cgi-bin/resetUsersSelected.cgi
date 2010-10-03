#!/bin/sh
# Modified By: Fernando F Nicola <nicolaff@gmail.com>
# To: Lugro-Mesh

# our html code
echo "<html>"
echo "<head><title>Base Settings Changed!</title></head>"
echo "<body>"
echo "$QUERY_STRING" | awk -F'&' -f clientDisconnect.awk
echo "</body>"
echo "</html>"
