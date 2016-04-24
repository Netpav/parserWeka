#!/usr/bin/perl
print "\n *********** \n";
for (glob '.\input\results_TP\*') {
#for ('en_50000.txt') {
	#next if $_ eq 'en_60000.txt';
	#print $_, $/;


	print "\n *********** \n";
	print $_;
	print "\n *********** \n";

system "python parse_cli_result.py $_";
#system "python parse_cli_result_Param.py $_"
system "python parse_cli_MOA_result_EvalTT.py $_";
system "python parse_cli_MOA_result_LearnModel.py $_";



}
