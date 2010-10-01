#!/bin/sh
# Copyright (C) 2005, 2006 Mikhail E. Zakharov
# Modified By: Fernando F Nicola <nicolaff@gmail.com>
# To: Lugro-Mesh

password=$1

fifo_in="/tmp/empty.in"			# input fifo
fifo_out="/tmp/empty.out"		# output

# -----------------------------------------------------------------------------
cmd="passwd"
#cmd="./testPass.sh"
tmp="/tmp/empty.tmp"			# tempfile to store results

empty -f -L $tmp -i $fifo_in -o $fifo_out $cmd
if [ $? = 0 ]; then
	if [ -w $fifo_in -a -r $fifo_out ]; then
		empty -w -v -i $fifo_out -o $fifo_in -t 10 assword: "$password\n"
		empty -w -v -i $fifo_out -o $fifo_in -t 10 Retype "$password\n"
	else
		echo "Error: Can't find I/O fifos!"
		exit 1
	fi
else
	echo "Error: Can't start empty in daemon mode"
	exit 1
fi
rm $fifo_in
rm $fifo_out
exit 0

