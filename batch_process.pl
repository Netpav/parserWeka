#!/usr/bin/perl

for (glob '.\input\Moa\*.*') {
#for ('en_50000.txt') {
	#next if $_ eq 'en_60000.txt';
	#print $_, $/;
	
	
	print "\n *********** \n";
	print $_;
	print "\n *********** \n";
	
system "python parse_cli_result.py $_";
system "python parse_cli_MOA_result.py $_";
system "python parse_cli_MOA_result_2.py $_";



}