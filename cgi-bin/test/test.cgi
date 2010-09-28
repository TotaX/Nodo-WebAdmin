#!/bin/sh

echo Content-type: text/html
echo ""

if [ $# = 0 ]
then
/bin/cat << EOM1
  <HTML>
  <HEAD><TITLE>Text search </TITLE>
  </HEAD>
  <BODY bgcolor="#cccccc" text="#000000">
  <HR SIZE=5>
  <H1>Text search </H1>
  <P>
  <ISINDEX prompt="Enter search string: " action="test.cgi">
  <P>
  </BODY>
  </HTML>
EOM1
else
/bin/cat << EOM2
  <HTML>
  <HEAD><TITLE>Search results for $* </TITLE>
  </HEAD>
  <BODY bgcolor="#cccccc" text="#000000">
  <HR SIZE=5>
  <H1>Search results for $* </H1>
  <HR SIZE=5>
  <P>
  <PRE>
EOM2

pepe
pepe
pepe
pep1
pep2
pep3
/bin/cat << EOM3
  </PRE>
  <P>
  </BODY>
  </HTML>
EOM3
fi
