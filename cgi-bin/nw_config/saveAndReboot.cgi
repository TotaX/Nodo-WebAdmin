#!/bin/sh
PATH=/bin:/usr/bin:/sbin:/usr/sbin
echo "Content-type: text/html"

#
#SCRIPT PARA TOMAR TODAS LAS CONFIGURACIONES
#

cat<<HEADER

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
	<meta HTTP-EQUIV="REFRESH" content="0; url=http://www.google.com">
</head>
<body  bgcolor="#ffffff" text="#0000aa" link="#ff0000" vlink="#ff5555" alink="#aaaaff" >
<P>
HEADER

cat<<MAIN
<b> $$ </b>
MAIN

cat<<FOOTER
	$(cat footer_html)
FOOTER
#exit 0
