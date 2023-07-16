#!/bin/bash

DIR=$1
ransomware=$2
xmlPath=$DIR/xmls
dotFilesPath=$DIR/dotFiles

mkdir -p $dotFilesPath/$ransomware
cd /home/spades/SPADE/bin
#sudo ./spade start
./spade control <<EOF
add analyzer CommandLine
add storage PostgreSQL
set storage PostgreSQL
add reporter ProcMon input=$xmlPath/$ransomware.XML
remove reporter ProcMon
exit
EOF
./spade query <<EOF
exit
EOF
./spade query <<EOF
list
%only_processes = type == 'Process'
\$all_processes = \$base.getVertex(%only_processes)
%rw_name = "name" like '$ransomware.exe'
\$rw_processes = \$all_processes.getVertex(%rw_name)
\$rw_activity = \$base.getLineage(\$rw_processes, 2, 'ancestors')
env unset exportLimit
export > $dotFilesPath/$ransomware/$ransomware.dot
dump all \$rw_activity
exit
EOF
./spade control <<EOF
remove storage PostgreSQL
EOF
#./spade stop
grep 'operation:ReadFile\|operation:WriteFile\|category:Read\sMetadata|category:Write\sMetadata' $dotFilesPath/$ransomware/$ransomware.dot > $dotFilesPath/$ransomware/$ransomware.txt
wc -l $dotFilesPath/$ransomware/$ransomware.txt >> $DIR/file_ops
./manage-postgres.sh clear

