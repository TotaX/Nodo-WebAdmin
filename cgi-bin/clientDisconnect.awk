#!/bin/awk -f
# Modified By: Fernando F Nicola <nicolaff@gmail.com>
# To: Lugro-Mesh
function disconnectUser(user_ip)
{ 
	CMD = "wdctl reset " user_ip
	CMD | getline RESULT
	if (RESULT ~ "successfully")
		print "Desconectando Ip USer:" CMD
	else
		print "No se pudo desconectar Usuario con IP: " user_ip
close(CMD)
}

function getUserIp(user_id)
{
	CMD="wdctl status"
	while((CMD | getline LINE)>0){
		a = match(LINE,"Client")
		b = match(LINE,user_id)
		if (a && b){
			if((CMD | getline IP_MAC) > 0)
			{
				split(IP_MAC,IP," ")
				break
			}
		}
	}
close(CMD)
return IP[2]
}
#MAIN PER LINE
{
	for(i=1;i<NF;i++)
	{
		split($i,VAR,/_/)
		split(VAR[2],USER_ID,/=/)
		ipUser = getUserIp(USER_ID[1])
		disconnectUser(ipUser)
	}
}
