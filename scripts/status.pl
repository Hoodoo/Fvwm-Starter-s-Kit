#!/usr/bin/perl

use warnings;
use strict;

my $song = "MPD Stopped";

$song = `mpc current`;

system `FvwmCommand \'SendToModule TopPanel ChangeButton MPDStatus Title \"$song\"\'`;

my $date = `date +"%a %b %d, %H:%M"`;

system `FvwmCommand \'SendToModule TopPanel ChangeButton Clock Title \"$date\"\'`;

my $emails = `cat /tmp/newmails`;

system `FvwmCommand \'SendToModule TopPanel ChangeButton Emails Title \"$emails\"\'`;

