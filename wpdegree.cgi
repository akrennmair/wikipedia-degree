#!/usr/bin/perl

use CGI;

$dir = "<insert path to wikipedia-degree checkout here>";
$tmpl = "wp-degree.tex.tmpl";

sub get_special_date() {
	my @date = localtime(time);
	my @months = ( "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" );
	my $mday = $date[3];
	my $month = $date[4];
	my $year = 1900 + $date[5];

	if ($mday >= 10 && $mday < 13) {
		$mday .= "th";
	} elsif ($mday%10 == 1) {
		$mday .= "st";
	} elsif ($mday%10 == 2) {
		$mday .= "nd";
	} elsif ($mday%10 == 3) {
		$mday .= "rd";
	} else {
		$mday .= "th";
	}

	return "$mday of $months[$month], $year";
}

$q = new CGI;

if ($q->param('name')) {
	$name = $q->param('name');
	$name =~ s/[\\@\{\}]//g;
	$date = get_special_date();

	open FILE, "$dir/$tmpl" or die "couldn't open $dir/$tmpl: $!";

	@lines = ();
	while ($line = <FILE>) {
		push(@lines, $line);
	}
	close FILE;

	@result = ();
	foreach $line (@lines) {
		$line =~ s/\@NAME\@/$name/g;
		$line =~ s/\@DATE\@/$date/g;
		push(@result, $line);
	}
	open OUTFILE, ">$dir/$tmpl-$$.tex" or die "couldn't open $dir/$tmpl-$$.tex: $!";
	foreach $line (@result) {
		print OUTFILE "$line";
	}
	close OUTFILE;

	chdir($dir);

	system("pdflatex $dir/$tmpl-$$.tex > /dev/null 2>&1");

	open PDF, "$dir/$tmpl-$$.pdf" or die "couldn't open $dir/$tmpl-$$.pdf: $!";
	binmode(PDF);
	$buffer = "";
	read(PDF, $buffer, 1024*1024*1024, 0);
	close(PDF);

	print $q->header(-type=>"application/pdf", -attachment=>"Wikipedia_Degree.pdf");

	print $buffer;

	system("rm", "-f", "$dir/$tmpl-$$.pdf", "$dir/$tmpl-$$.tex", "$dir/$tmpl-$$.aux", "$dir/$tmpl-$$.log");
} else {
	print $q->header;
	print "<html><head><title>Wikipedia Degree Generator</title></head></body><h1>Wikipedia Degree Generator</h1>\n";
	print $q->start_form('get'), "Your name? ", $q->textfield(-name=>"name"), $q->submit(-value=>"Get me a degree!"), $q->end_form;
	print "</html>";
}
