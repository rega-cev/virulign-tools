#!/bin/sh

#!!!Important: this script requires the insdseqget binary 
#(part of the NCBI tools, can be downloaded from here: ftp://ftp.ncbi.nih.gov/toolbox/ncbi_tools/converters/)

#insdseqget command path
insdseqget_cmd=$1
#genbank entry name as arg
genbank_entry=$2

#TODO
#create file on stdin where the entry is stored in

${insdseqget_cmd} <<< ${genbank_entry}
