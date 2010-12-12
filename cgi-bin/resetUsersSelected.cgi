#!/bin/sh
# Modified By: Fernando F Nicola <nicolaff@gmail.com>
# To: LUGRo-Mesh

# our html code
echo -e "Content-type: text/html\n\n"
cat << HEADER
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <title>Nightwing: Client Info</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
	<META NAME="Author" CONTENT="Fernando F Nicola"> 
	<META NAME="description" CONTENT="LUGRo-Mesh Node Admin|Client Status And Disconnect">
	<META NAME="Copyright" CONTENT="LUGRo-Mesh (C) 2008-2010.">
    <link rel="stylesheet" type="text/css" href="../style.css">
    <link rel="stylesheet" type="text/css" href="../niftyCorners.css">
    <script type="text/javascript" src="../niftycube.js"></script>
    <script type="text/javascript">
      window.onload=function(){
          Nifty("ul#nav a","small transparent top");
          Nifty("div#box","big");
      }
      function delayer(){
      if(!window.location.toString().match(/clientOnLine/)){
      	    window.location =  "/cgi-bin/clientOnLine.html"
      	    window.location.replace();
      	}
      }
    </script>
  </head>
  <body onLoad="setTimeout('delayer()',5000)">
    <div id="menu">
      <ul id="nav">
        <li id="home"><a href="/">Home</a></li>
        <li id="info"><a href="info.html">Info</a></li>
	<li id="cs"  class="activelink"><a href="clientOnLine.html">Client Status</a></li>
	<li id="nw_conf"> <a href="nw_config/nw_conf_web.html">Config</a></li>
	<li id="mac_admin"> <a href="mac_admin/mac_admin.html">MAC Admin</a></li>
      </ul>
    </div>
HEADER

cat << MAIN
<div id="box">     
$(echo "$QUERY_STRING" | awk -F'&' -f /www/cgi-bin/clientDisconnect.awk)
</div>
MAIN

cat << FOOTER
<p></p>                                                                                                                                             
<div id="footer">                                                                                                                                   
<center>                                                                                                                                            
        <p>Nightwing by <a href="http://www.lugro-mesh.org.ar/>LUGRo-Mesh</a></p>                                                                   
</center>                                                                                                                             
</div>                                                                                                                                              
</body>                                                                                                                                             
</html>
FOOTER
