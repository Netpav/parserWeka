#!/usr/bin/perl

for (glob '.\input\cli\en_*') {
#for ('en_50000.txt') {
	#next if $_ eq 'en_60000.txt';
	#print $_, $/;
	
	
	print "\n *********** \n";
	print $_;
	print "\n *********** \n";
	
system "python parse_cli_result.py $_";


}