#!/usr/bin/perl

use warnings;
use strict;

my $icon;

system("mpc toggle");
my $mpds = `mpc | grep -c paused`;

if ($mpds == 1){
    system `FvwmCommand \'SendToModule TopPanel ChangeButton MPDPP Icon \"media-playback-start.png\"\'`;
} else {
system `FvwmCommand \'SendToModule TopPanel ChangeButton MPDPP Icon \"media-playback-stop.png\"\'`;
}
